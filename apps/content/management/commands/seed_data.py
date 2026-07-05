from django.core.management.base import BaseCommand
# pyrefly: ignore [missing-import]
from apps.content.models import MealPlan, Routine, Resource, DailyQuote

class Command(BaseCommand):
    help = 'Seeds the database with initial PCOS meal plans, routines, resources, and quotes.'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        
        # 1. Seed Daily Quotes
        quotes = [
            ("Your illness does not define you. Your strength and courage do.", "Unknown"),
            ("Wellness is a connection of paths: physical, mental, and emotional. Nourish all of them.", "Unknown"),
            ("Small daily changes lead to massive long-term results. Be patient with yourself.", "Unknown"),
            ("Healing is not linear. Embrace the journey and honor what your body tells you.", "Unknown"),
            ("PCOS is a chapter in your life, not the whole book. You have the power to write the ending.", "Unknown"),
            ("Every healthy choice you make today is an investment in your tomorrow.", "Unknown"),
        ]
        
        for text, author in quotes:
            DailyQuote.objects.get_or_create(quote=text, author=author)
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(quotes)} quotes.'))

        # 2. Seed Routines (Workout, Yoga, Meditation)
        routines = [
            # Workouts
            {
                'category': 'Workout',
                'title': 'Low-Impact Strength Training',
                'subtitle': '25 mins • Beginner',
                'difficulty': 'Beginner',
                'duration_minutes': 25,
                'description': 'A full-body strength routine designed to build muscle and increase insulin sensitivity without raising cortisol levels excessively.',
                'steps': [
                    'Warm-up: 5 minutes of gentle walking or dynamic stretching (arm circles, torso twists).',
                    'Bodyweight Squats: 3 sets of 10 reps (slow and controlled).',
                    'Wall Push-Ups or Incline Push-Ups: 3 sets of 8 reps.',
                    'Glute Bridges: 3 sets of 12 reps (squeeze glutes at the top).',
                    'Bird-Dog: 3 sets of 8 reps per side (focus on core stability).',
                    'Cool-down: 5 minutes of static stretching (hamstring stretch, child\'s pose).'
                ]
            },
            {
                'category': 'Workout',
                'title': 'Steady-State Cardio Walk',
                'subtitle': '30 mins • Beginner',
                'difficulty': 'Beginner',
                'duration_minutes': 30,
                'description': 'An outdoor or treadmill walking routine maintained at a conversational pace. Excellent for cardiovascular health and lowering stress hormones.',
                'steps': [
                    'Warm-up: 3 minutes walking at a slow pace.',
                    'Main walk: 24 minutes walking at a brisk, conversational pace (you can talk but not sing).',
                    'Cool-down: 3 minutes walking at a slow, relaxing pace to lower your heart rate.'
                ]
            },
            # Yoga
            {
                'category': 'Yoga',
                'title': 'Restorative Yoga for Pelvic Blood Flow',
                'subtitle': '20 mins • All Levels',
                'difficulty': 'Beginner',
                'duration_minutes': 20,
                'description': 'A series of gentle yoga poses focusing on the hips and pelvis to improve circulation, relieve menstrual cramps, and promote deep relaxation.',
                'steps': [
                    'Child\'s Pose (Balasana) - Hold for 3 minutes (deep belly breathing).',
                    'Bound Angle Pose (Baddha Konasana) - Hold for 3 minutes.',
                    'Supine Butterfly Pose (Supta Baddha Konasana) - Support knees with pillows. Hold for 5 minutes.',
                    'Legs-Up-The-Wall Pose (Viparita Karani) - Hold for 5 minutes (relieves fatigue).',
                    'Corpse Pose (Savasana) - Spend 4 minutes in quiet stillness.'
                ]
            },
            # Meditation
            {
                'category': 'Meditation',
                'title': 'Cortisol-Lowering Breathing Practice',
                'subtitle': '10 mins • Mindful Breathing',
                'difficulty': 'Beginner',
                'duration_minutes': 10,
                'description': 'A guided box breathing technique designed to shift your autonomic nervous system from sympathetic (fight or flight) to parasympathetic (rest and digest).',
                'steps': [
                    'Find a comfortable seated position with your spine erect and shoulders relaxed.',
                    'Inhale slowly through your nose for a count of 4, filling your chest and abdomen.',
                    'Hold your breath gently for a count of 4.',
                    'Exhale slowly and smoothly through your mouth for a count of 4, emptying your lungs.',
                    'Hold your breath empty for a count of 4.',
                    'Repeat this cycle (box breathing) for 8 minutes.',
                    'Rest in normal breathing for 1-2 minutes, observing the calm state of your mind.'
                ]
            }
        ]

        for r_data in routines:
            Routine.objects.get_or_create(
                category=r_data['category'],
                title=r_data['title'],
                defaults={
                    'subtitle': r_data['subtitle'],
                    'difficulty': r_data['difficulty'],
                    'duration_minutes': r_data['duration_minutes'],
                    'description': r_data['description'],
                    'steps': r_data['steps']
                }
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(routines)} routines.'))

        # 3. Seed Educational Resources
        resources = [
            {
                'category': 'Basics',
                'title': 'Understanding PCOS and Insulin Resistance',
                'summary': 'Learn the core mechanism behind PCOS symptoms and why managing blood sugar is key to healing.',
                'content': (
                    '# Understanding PCOS and Insulin Resistance\n\n'
                    'Polycystic Ovary Syndrome (PCOS) is a hormonal imbalance that affects millions of women worldwide. '
                    'While its symptoms are wide-ranging (including irregular periods, acne, thinning hair, and weight changes), '
                    'one of the most common underlying drivers is **insulin resistance**.\n\n'
                    '## What is Insulin Resistance?\n'
                    'Insulin is a hormone produced by your pancreas that acts like a key, unlocking your cells so they can absorb glucose (sugar) from your bloodstream for energy. '
                    'When you have insulin resistance, your cells resist this signal. As a result, your pancreas has to pump out *more* insulin to keep blood sugar normal.\n\n'
                    '## How does High Insulin affect PCOS?\n'
                    'Excessive insulin in the bloodstream triggers two major responses that worsen PCOS:\n'
                    '1. **Stimulates Androgen Production**: High insulin tells the ovaries to produce more male hormones like testosterone. This leads to symptoms like hirsutism (excess hair), hormonal acne, and male-pattern hair loss.\n'
                    '2. **Prevents Ovulation**: Elevated androgens disrupt follicular development in the ovaries, preventing a follicle from maturing and releasing an egg (causing skipped or irregular periods).\n'
                    '3. **Promotes Fat Storage**: Insulin is a storage hormone. High levels make it easier for the body to store fat (especially around the abdomen) and make weight loss more challenging.\n\n'
                    '## The Good News\n'
                    'Because insulin resistance is a major driver, dietary and lifestyle choices that improve insulin sensitivity can radically reduce PCOS symptoms. '
                    'Focusing on low-glycemic, fiber-rich, and protein-packed meals combined with gentle strength training can make a profound difference.'
                )
            },
            {
                'category': 'Nutrition',
                'title': 'The PCOS Anti-Inflammatory Plate',
                'summary': 'A practical guide to structuring your meals to reduce inflammation and support hormone balance.',
                'content': (
                    '# The PCOS Anti-Inflammatory Plate\n\n'
                    'Chronic low-grade inflammation is another major driver of PCOS. Working hand-in-hand with insulin resistance, inflammation can impair ovulation and increase adrenal androgen production. '
                    'Eating a nutrient-dense, anti-inflammatory diet is one of the most powerful tools to heal from the inside out.\n\n'
                    '## Key Principles of the PCOS Plate\n'
                    'Instead of restrictive diets or counting calories, focus on adding hormone-supportive ingredients to your plate. Aim for this composition at major meals:\n\n'
                    '### 1. Half Plate: Non-Starchy Vegetables (Fiber & Antioxidants)\n'
                    '* Leafy greens (spinach, kale, arugula)\n'
                    '* Cruciferous vegetables (broccoli, cauliflower, Brussels sprouts)\n'
                    '* Bell peppers, zucchini, cucumber, asparagus\n'
                    '* *Why?* Fiber slows down digestion, preventing blood sugar spikes, while antioxidants fight cell inflammation.\n\n'
                    '### 2. One-Quarter Plate: High-Quality Protein\n'
                    '* Wild-caught fish (salmon, mackerel, sardines - rich in Omega-3s)\n'
                    '* Organic chicken, turkey, or lean beef\n'
                    '* Eggs, tofu, or tempeh\n'
                    '* *Why?* Protein is crucial for muscle repair, increases satiety hormones, and prevents blood sugar spikes.\n\n'
                    '### 3. One-Quarter Plate: Slow-Burning Complex Carbs\n'
                    '* Quinoa, brown rice, wild rice\n'
                    '* Sweet potato, squash, pumpkin\n'
                    '* Legumes (lentils, chickpeas, black beans)\n'
                    '* *Why?* Complex carbs retain fiber and nutrients, releasing energy slowly without spiking insulin.\n\n'
                    '### 4. Healthy Fats (The Hormone Building Blocks)\n'
                    '* Avocado, extra virgin olive oil, olives\n'
                    '* Nuts (walnuts, almonds) and seeds (chia, flax, pumpkin)\n'
                    '* *Why?* Healthy fats are required for hormone synthesis, reduce inflammation, and help keep you full for hours.'
                )
            }
        ]

        for res in resources:
            Resource.objects.get_or_create(
                title=res['title'],
                defaults={
                    'category': res['category'],
                    'summary': res['summary'],
                    'content': res['content']
                }
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(resources)} resources.'))

        # 4. Seed Meal Plans (Week 1, Monday to Sunday)
        # We will create 1 week rotation of meals.
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_indices = {day: idx for idx, day in enumerate(days)}

        meal_templates = {
            'Monday': [
                ('Breakfast', 'Spinach & Mushroom Scramble with Avocado', '3 large eggs scrambled with a handful of fresh spinach, cremini mushrooms, and topped with 1/4 sliced avocado. Served with a slice of gluten-free seed toast.', 380, 15, 24, 26, ['Eggs', 'Spinach', 'Mushrooms', 'Avocado', 'Seed toast']),
                ('Lunch', 'Quinoa Salad with Salmon and Lemon Dressing', 'Flaked grilled salmon over cooked quinoa, tossed with chopped cucumber, cherry tomatoes, parsley, and olive oil/lemon juice dressing.', 520, 38, 30, 22, ['Salmon', 'Quinoa', 'Cucumber', 'Cherry tomatoes', 'Olive oil', 'Lemon']),
                ('Dinner', 'Anti-Inflammatory Turmeric Chicken & Broccoli', 'Chicken breast cubes sautéed in extra virgin olive oil with minced garlic, ginger, and turmeric. Served with roasted broccoli florets and brown rice.', 480, 42, 38, 14, ['Chicken breast', 'Broccoli', 'Brown rice', 'Turmeric', 'Ginger', 'Olive oil']),
                ('Snack', 'Pumpkin Seed & Apple Slices', 'One medium organic green apple sliced, paired with a small handful (approx. 30g) of raw pumpkin seeds.', 180, 22, 10, 6, ['Apple', 'Pumpkin seeds'])
            ],
            'Tuesday': [
                ('Breakfast', 'Chia Seed Pudding with Berries', 'Chia seeds soaked overnight in unsweetened almond milk with vanilla extract. Topped with fresh raspberries, blueberries, and chopped walnuts.', 320, 24, 18, 8, ['Chia seeds', 'Almond milk', 'Raspberries', 'Blueberries', 'Walnuts']),
                ('Lunch', 'Leftover Turmeric Chicken & Salad', 'Leftover turmeric chicken from Monday dinner served over a large bed of mixed baby greens, cucumbers, pumpkin seeds, and a splash of olive oil.', 410, 12, 18, 32, ['Chicken breast', 'Mixed greens', 'Cucumber', 'Pumpkin seeds', 'Olive oil']),
                ('Dinner', 'Baked Cod with Roasted Sweet Potato & Asparagus', 'Wild-caught cod fillet seasoned with herbs and baked. Served with a side of roasted sweet potato wedges and grilled asparagus.', 440, 32, 12, 28, ['Cod fillet', 'Sweet potato', 'Asparagus', 'Herbs']),
                ('Snack', 'Cucumber Slices with Hummus', 'One whole cucumber sliced, served with 3 tablespoons of organic sesame hummus.', 140, 16, 6, 4, ['Cucumber', 'Hummus'])
            ],
            'Wednesday': [
                ('Breakfast', 'Protein-Packed Berry Smoothie', 'One scoop of pea protein powder blended with unsweetened almond milk, a handful of frozen blueberries, spinach, and 1 tablespoon of ground flaxseed.', 290, 18, 8, 24, ['Pea protein', 'Almond milk', 'Blueberries', 'Spinach', 'Flaxseed']),
                ('Lunch', 'Quinoa & Black Bean Buddha Bowl', 'Bowl with cooked quinoa, organic black beans, steamed spinach, shredded carrots, and a tahini lemon dressing.', 460, 52, 14, 15, ['Quinoa', 'Black beans', 'Spinach', 'Carrots', 'Tahini', 'Lemon']),
                ('Dinner', 'Turkey Stir-Fry with Cauliflower Rice', 'Lean ground turkey cooked with mixed stir-fry vegetables (snap peas, bell peppers, carrots) in coconut aminos, served over cauliflower rice.', 390, 18, 15, 34, ['Ground turkey', 'Mixed vegetables', 'Cauliflower rice', 'Coconut aminos']),
                ('Snack', 'Walnuts & Dark Chocolate (85%+)', 'A small handful of walnuts paired with 2 squares of high-quality 85% dark chocolate.', 210, 10, 16, 4, ['Walnuts', 'Dark chocolate'])
            ],
            'Thursday': [
                ('Breakfast', 'Spinach & Mushroom Scramble with Avocado', '3 large eggs scrambled with a handful of fresh spinach, cremini mushrooms, and topped with 1/4 sliced avocado. Served with a slice of gluten-free seed toast.', 380, 15, 24, 26, ['Eggs', 'Spinach', 'Mushrooms', 'Avocado', 'Seed toast']),
                ('Lunch', 'Leftover Turkey Stir-Fry', 'Leftover turkey stir-fry from Wednesday dinner served over warm cauliflower rice.', 390, 18, 15, 34, ['Ground turkey', 'Mixed vegetables', 'Cauliflower rice']),
                ('Dinner', 'Grilled Salmon with Quinoa & Green Beans', 'Fresh salmon fillet grilled and served with a side of steamed green beans and cooked quinoa.', 530, 36, 28, 35, ['Salmon', 'Green beans', 'Quinoa']),
                ('Snack', 'Boiled Eggs & Celery Sticks', 'Two hard-boiled eggs seasoned with sea salt and black pepper, served with fresh celery sticks.', 170, 4, 11, 13, ['Eggs', 'Celery'])
            ],
            'Friday': [
                ('Breakfast', 'Chia Seed Pudding with Berries', 'Chia seeds soaked overnight in unsweetened almond milk with vanilla extract. Topped with fresh raspberries, blueberries, and chopped walnuts.', 320, 24, 18, 8, ['Chia seeds', 'Almond milk', 'Raspberries', 'Blueberries', 'Walnuts']),
                ('Lunch', 'Mixed Greens Salad with Tuna & Olive Oil', 'Canned wild tuna mixed with olive oil, red onion, celery, and served over a large bed of leafy greens, topped with pumpkin seeds.', 390, 10, 22, 28, ['Tuna', 'Mixed greens', 'Celery', 'Olive oil', 'Pumpkin seeds']),
                ('Dinner', 'Beef & Vegetable Skewers with Sweet Potato', 'Lean beef cubes skewered with bell peppers and onions, grilled. Served with roasted sweet potato.', 470, 34, 18, 30, ['Lean beef', 'Bell peppers', 'Onion', 'Sweet potato']),
                ('Snack', 'Apple Slices with Almond Butter', 'One medium organic green apple sliced, paired with 1 tablespoon of raw almond butter.', 190, 22, 12, 3, ['Apple', 'Almond butter'])
            ],
            'Saturday': [
                ('Breakfast', 'Avocado Toast with Poached Eggs', 'Two poached eggs served on top of mashed avocado spread over toasted gluten-free seed bread, sprinkled with red pepper flakes.', 360, 22, 20, 18, ['Eggs', 'Avocado', 'Seed bread', 'Red pepper flakes']),
                ('Lunch', 'Leftover Beef & Veggie Skewers', 'Leftover grilled beef skewers and sweet potato from Friday dinner.', 470, 34, 18, 30, ['Lean beef', 'Bell peppers', 'Sweet potato']),
                ('Dinner', 'Baked Chicken Breast with Roasted Asparagus & Cauliflower Mashed', 'Chicken breast seasoned with rosemary and garlic, baked. Served with roasted asparagus and garlic cauliflower mash.', 420, 14, 16, 38, ['Chicken breast', 'Asparagus', 'Cauliflower', 'Rosemary', 'Garlic']),
                ('Snack', 'Mixed Berries & Pecans', 'A cup of fresh mixed berries paired with a small handful of raw pecan halves.', 160, 14, 12, 2, ['Mixed berries', 'Pecans'])
            ],
            'Sunday': [
                ('Breakfast', 'Protein-Packed Berry Smoothie', 'One scoop of pea protein powder blended with unsweetened almond milk, a handful of frozen blueberries, spinach, and 1 tablespoon of ground flaxseed.', 290, 18, 8, 24, ['Pea protein', 'Almond milk', 'Blueberries', 'Spinach', 'Flaxseed']),
                ('Lunch', 'Mediterranean Salad with Chickpeas & Feta', 'Chopped cucumber, cherry tomatoes, olives, red onion, and organic chickpeas tossed in olive oil, topped with 30g of crumbled feta cheese.', 430, 36, 22, 12, ['Cucumber', 'Cherry tomatoes', 'Olives', 'Chickpeas', 'Olive oil', 'Feta cheese']),
                ('Dinner', 'Slow Cooker Lemon Herb Chicken with Roasted Zucchini', 'Slow-cooked chicken thigh seasoned with lemon, oregano, and garlic, served with sliced zucchini roasted in olive oil.', 410, 8, 25, 30, ['Chicken thighs', 'Zucchini', 'Lemon', 'Oregano', 'Olive oil']),
                ('Snack', 'Pumpkin Seeds', 'A small bowl (30g) of dry roasted pumpkin seeds.', 150, 4, 12, 7, ['Pumpkin seeds'])
            ]
        }

        # Seed Week 1 Meal Plan
        meal_count = 0
        for day, meals in meal_templates.items():
            day_idx = day_indices[day]
            for m_type, name, desc, cals, carbs, fat, prot, ingredients in meals:
                MealPlan.objects.get_or_create(
                    week_number=1,
                    day_of_week=day_idx,
                    meal_type=m_type,
                    defaults={
                        'name': name,
                        'description': desc,
                        'calories': cals,
                        'carbs_g': carbs,
                        'fat_g': fat,
                        'protein_g': prot,
                        'ingredients': ingredients,
                        'is_pcos_friendly': True
                    }
                )
                meal_count += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {meal_count} meals for Week 1.'))

        # Seed Week 2 Meal Plan (Anti-inflammatory variations)
        week2_templates = {
            'Monday': [
                ('Breakfast', 'Hormone-Balancing Green Smoothie', 'Blended kale, mango cubes, unsweetened almond milk, organic hemp seeds, and a scoop of pea protein powder.', 310, 18, 9, 22, ['Kale', 'Mango', 'Almond milk', 'Hemp seeds', 'Pea protein']),
                ('Lunch', 'Warm Lentil & Spinach Salad with Chicken', 'Cooked green lentils served warm over baby spinach, sliced chicken breast, walnuts, and a light lemon-balsamic dressing.', 490, 32, 16, 38, ['Lentils', 'Spinach', 'Chicken breast', 'Walnuts', 'Balsamic vinegar']),
                ('Dinner', 'Lemon Herb Baked Salmon with Roasted Broccoli', 'Wild-caught salmon baked with fresh rosemary, garlic, and lemon slices. Served with roasted broccoli and half a cup of wild rice.', 510, 24, 28, 36, ['Salmon', 'Broccoli', 'Wild rice', 'Lemon', 'Garlic']),
                ('Snack', 'Pecan Halves & Fresh Raspberries', 'A small handful of pecans paired with half a cup of fresh raspberries.', 170, 8, 14, 2, ['Pecans', 'Raspberries'])
            ],
            'Tuesday': [
                ('Breakfast', 'Gluten-Free Oats with Flax & Cinnamon', 'Steel-cut oats cooked in water, mixed with ground flaxseed, almond milk, cinnamon, and raw pumpkin seeds.', 290, 36, 10, 8, ['Gluten-free oats', 'Flaxseed', 'Almond milk', 'Cinnamon', 'Pumpkin seeds']),
                ('Lunch', 'Leftover Lemon Herb Salmon with Wild Rice', 'Leftover salmon, broccoli, and wild rice from Monday dinner.', 510, 24, 28, 36, ['Salmon', 'Broccoli', 'Wild rice']),
                ('Dinner', 'Anti-Inflammatory Turmeric Turkey Burgers', 'Lean ground turkey patties seasoned with turmeric, cumin, and garlic, wrapped in fresh romaine lettuce leaves and served with sweet potato wedges.', 450, 28, 14, 32, ['Ground turkey', 'Turmeric', 'Lettuce wraps', 'Sweet potato']),
                ('Snack', 'Hummus with Carrot & Cucumber Sticks', 'Sesame tahini hummus paired with fresh baby carrot and cucumber sticks.', 130, 15, 6, 3, ['Hummus', 'Carrots', 'Cucumber'])
            ],
            'Wednesday': [
                ('Breakfast', 'Garden Vegetable Omelet', '3 organic eggs folded with sautéed bell peppers, spinach, onions, and diced tomatoes, cooked in extra virgin olive oil.', 340, 6, 22, 24, ['Eggs', 'Bell peppers', 'Spinach', 'Onion', 'Tomato', 'Olive oil']),
                ('Lunch', 'Leftover Turmeric Turkey Burgers', 'Turkey burger patty wrapped in lettuce leaves, served with sweet potato wedges.', 450, 28, 14, 32, ['Ground turkey', 'Lettuce wraps', 'Sweet potato']),
                ('Dinner', 'Quinoa Bowl with Sesame Tofu & Brussels Sprouts', 'Cooked quinoa topped with pan-seared organic tofu cubes, roasted Brussels sprouts, and a splash of sesame ginger dressing.', 420, 48, 16, 18, ['Quinoa', 'Tofu', 'Brussels sprouts', 'Sesame oil', 'Ginger']),
                ('Snack', 'Walnuts & Sliced Green Apple', 'A handful of raw walnuts paired with half a sliced green apple.', 190, 16, 12, 3, ['Walnuts', 'Apple'])
            ],
            'Thursday': [
                ('Breakfast', 'Hormone-Balancing Green Smoothie', 'Blended kale, mango cubes, unsweetened almond milk, organic hemp seeds, and a scoop of pea protein powder.', 310, 18, 9, 22, ['Kale', 'Mango', 'Almond milk', 'Hemp seeds', 'Pea protein']),
                ('Lunch', 'Tuna Salad Avocado Boats', 'Wild-caught canned tuna mixed with olive oil, celery, and red onion, stuffed inside two halved avocados.', 430, 8, 32, 24, ['Tuna', 'Avocado', 'Celery', 'Olive oil']),
                ('Dinner', 'Grilled Chicken & Veggie Skewers with Brown Rice', 'Chicken breast cubes skewered with red bell peppers, zucchini, and red onion, grilled and served with half a cup of brown rice.', 460, 32, 12, 35, ['Chicken breast', 'Bell peppers', 'Zucchini', 'Onion', 'Brown rice']),
                ('Snack', 'Hard-Boiled Eggs with Salt & Pepper', 'Two organic hard-boiled eggs sprinkled with sea salt and black pepper.', 140, 1, 10, 12, ['Eggs'])
            ],
            'Friday': [
                ('Breakfast', 'Gluten-Free Oats with Flax & Cinnamon', 'Steel-cut oats cooked in water, mixed with ground flaxseed, almond milk, cinnamon, and raw pumpkin seeds.', 290, 36, 10, 8, ['Gluten-free oats', 'Flaxseed', 'Almond milk', 'Cinnamon', 'Pumpkin seeds']),
                ('Lunch', 'Leftover Chicken Veggie Skewers with Rice', 'Leftover grilled chicken skewers and brown rice from Thursday dinner.', 460, 32, 12, 35, ['Chicken breast', 'Bell peppers', 'Zucchini', 'Brown rice']),
                ('Dinner', 'Baked Cod with Olive Tapenade & Asparagus', 'Baked cod fillet topped with a tapenade of black olives, capers, and olive oil, served with grilled asparagus.', 380, 8, 22, 28, ['Cod fillet', 'Olives', 'Capers', 'Olive oil', 'Asparagus']),
                ('Snack', 'Raw Pistachios & Dark Chocolate (90%)', 'A small handful of raw pistachios paired with 1 square of 90% dark chocolate.', 180, 8, 12, 4, ['Pistachios', 'Dark chocolate'])
            ],
            'Saturday': [
                ('Breakfast', 'Scrambled Eggs with Smoked Salmon', '3 eggs scrambled with baby spinach, topped with 50g flaked smoked salmon and fresh dill, served with gluten-free seed toast.', 390, 16, 24, 28, ['Eggs', 'Smoked salmon', 'Spinach', 'Dill', 'Seed toast']),
                ('Lunch', 'Quinoa & Lentil Tabbouleh', 'Cooked quinoa and green lentils tossed with chopped parsley, tomatoes, cucumber, green onions, fresh mint, and extra virgin olive oil.', 410, 42, 15, 14, ['Quinoa', 'Lentils', 'Parsley', 'Tomato', 'Cucumber', 'Olive oil']),
                ('Dinner', 'Grass-Fed Beef Stir-Fry with Bok Choy', 'Sliced beef sirloin sautéed in sesame oil with ginger, garlic, shiitake mushrooms, and bok choy, served over cauliflower rice.', 450, 12, 25, 32, ['Beef sirloin', 'Bok choy', 'Mushrooms', 'Sesame oil', 'Cauliflower rice']),
                ('Snack', 'Coconut Chia Seed Pudding', 'Chia seeds soaked in light coconut milk, topped with fresh blueberries.', 210, 14, 12, 3, ['Chia seeds', 'Coconut milk', 'Blueberries'])
            ],
            'Sunday': [
                ('Breakfast', 'Protein Berry Pancakes (GF)', 'Gluten-free pancake made from oat flour, pea protein, mashed banana, and egg, topped with fresh warm blueberries.', 330, 42, 6, 18, ['Oat flour', 'Pea protein', 'Banana', 'Egg', 'Blueberries']),
                ('Lunch', 'Leftover Beef Stir-Fry with Bok Choy', 'Leftover beef stir-fry and cauliflower rice from Saturday dinner.', 450, 12, 25, 32, ['Beef sirloin', 'Bok choy', 'Mushrooms', 'Cauliflower rice']),
                ('Dinner', 'Roasted Turkey Breast with Sweet Potato Mash', 'Roasted turkey breast served with mashed sweet potatoes and steam-cooked green beans with olive oil.', 430, 36, 10, 34, ['Turkey breast', 'Sweet potato', 'Green beans', 'Olive oil']),
                ('Snack', 'Dry Roasted Sunflower Seeds', 'A small bowl (30g) of raw or dry-roasted sunflower seeds.', 160, 6, 14, 6, ['Sunflower seeds'])
            ]
        }

        week2_meal_count = 0
        for day, meals in week2_templates.items():
            day_idx = day_indices[day]
            for m_type, name, desc, cals, carbs, fat, prot, ingredients in meals:
                MealPlan.objects.get_or_create(
                    week_number=2,
                    day_of_week=day_idx,
                    meal_type=m_type,
                    defaults={
                        'name': name,
                        'description': desc,
                        'calories': cals,
                        'carbs_g': carbs,
                        'fat_g': fat,
                        'protein_g': prot,
                        'ingredients': ingredients,
                        'is_pcos_friendly': True
                    }
                )
                week2_meal_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {week2_meal_count} meals for Week 2.'))
        self.stdout.write(self.style.SUCCESS('All seeding completed successfully!'))
