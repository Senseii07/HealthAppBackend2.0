import logging
# pyrefly: ignore [missing-import]
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
# pyrefly: ignore [missing-import]
import google.generativeai as genai

# pyrefly: ignore [missing-import]
from apps.chat.models import ChatSession, ChatMessage
# pyrefly: ignore [missing-import]
from apps.chat.serializers import ChatSessionSerializer, ChatMessageSerializer

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are a warm, empathetic, and professional PCOS wellness assistant. "
    "Your goal is to help the user manage their PCOS/PCOD symptoms through nutrition, lifestyle changes, "
    "gentle exercise, stress relief, and habit formation. "
    "Always maintain an encouraging and positive tone.\n\n"
    "CRITICAL SAFETY GUIDELINES:\n"
    "1. You are a wellness companion, NOT a medical doctor. Do not make medical diagnoses, prescribe drugs, "
    "or recommend altering medical therapies.\n"
    "2. If the user presents medical emergencies, severe symptoms (like sharp abdominal pain, extreme bleeding), "
    "or asks about medications, advise them directly to consult their healthcare provider or gynecologist.\n"
    "3. Keep advice focused on gentle exercise, anti-inflammatory food options, sleep, and emotional wellbeing."
)

class ChatSessionViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        session = self.get_object()
        user_content = request.data.get('content', '').strip()
        
        if not user_content:
            return Response({'error': 'Content is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Save user's message
        user_message = ChatMessage.objects.create(
            session=session,
            role='user',
            content=user_content
        )

        # Update session title if it's the first message
        if not session.title or session.title == 'New Chat':
            session.title = user_content[:40] + ('...' if len(user_content) > 40 else '')
            session.save()

        # 2. Query Gemini API
        assistant_response = ""
        api_key = getattr(settings, 'GEMINI_API_KEY', '')

        if not api_key:
            assistant_response = (
                "Hi there! I am your PCOS Companion AI. It looks like the Gemini API key has not been "
                "configured in the backend environment yet. Please add a valid GEMINI_API_KEY to the "
                "backend .env file to enable live conversation."
            )
        elif api_key == "AQ.Ab8RN6IunaJggq-e2ocyLNICZNOeh1NMMdkvNvN4KONDN7Y6SQ":
            assistant_response = (
                "Hi there! It looks like you are using the placeholder GEMINI_API_KEY from the .env.example template. "
                "Please replace it with a valid API key from Google AI Studio in your backend .env file to enable the AI assistant."
            )
        else:
            try:
                genai.configure(api_key=api_key)
                # Use gemini-2.5-flash for current compatibility and active quota limits
                model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash",
                    system_instruction=SYSTEM_PROMPT
                )
                
                # Fetch recent messages for context (last 8 messages)
                recent_msgs = session.messages.all().order_by('-created_at')[:9] # includes user's latest
                recent_msgs = reversed(recent_msgs)
                
                gemini_history = []
                for msg in recent_msgs:
                    # Ignore the current user message since it will be passed to send_message
                    if msg.id == user_message.id:
                        continue
                    role = 'user' if msg.role == 'user' else 'model'
                    gemini_history.append({
                        'role': role,
                        'parts': [msg.content]
                    })
                
                # Start chat with history
                chat = model.start_chat(history=gemini_history)
                response = chat.send_message(user_content)
                assistant_response = response.text
            except Exception as e:
                logger.error(f"Gemini API error: {str(e)}")
                if "invalid authentication" in str(e).lower() or "401" in str(e) or "api key" in str(e).lower():
                    assistant_response = (
                        "The Gemini API key configured in the backend .env file is invalid or expired. "
                        "Please verify your key in Google AI Studio and update the GEMINI_API_KEY setting."
                    )
                else:
                    assistant_response = (
                        "I apologize, but I encountered an issue connecting to my AI core. "
                        "Please try again in a moment, or ask your administrator to check the Gemini API logs."
                    )

        # 3. Save assistant's response
        ChatMessage.objects.create(
            session=session,
            role='assistant',
            content=assistant_response
        )

        # Return updated session details
        serializer = self.get_serializer(session)
        return Response(serializer.data, status=status.HTTP_200_OK)
