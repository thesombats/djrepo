import random
from django.contrib.auth.models import User
from main.models import Resume, Skill, Education, PreviousJob, Company, Rating
from faker import Faker

def generate_fake_resumes(count):
    fake = Faker()
    
    # Ensure some companies exist
    if not Company.objects.exists():
        for _ in range(20):
            Company.objects.create(
                name=fake.company(),
                location=fake.city(),
                description=fake.catch_phrase()
            )
    
    companies = list(Company.objects.all())
    
    # Predefined skills for variety
    skill_pool = [
        "Python", "Django", "JavaScript", "React", "Vue", "SQL", "PostgreSQL",
        "Docker", "Kubernetes", "AWS", "Azure", "GCP", "HTML", "CSS",
        "Machine Learning", "Data Analysis", "Project Management", "Agile",
        "Scrum", "Java", "C++", "C#", "Go", "Rust", "Swift", "Kotlin"
    ]

    degrees = [
        "B.S. in Computer Science", "M.S. in Data Science", 
        "B.A. in Business Administration", "MBA",
        "B.E. in Software Engineering", "Ph.D. in Artificial Intelligence",
        "B.Sc. in Information Technology"
    ]

    new_users = []
    for i in range(count):
        username = f"user_{fake.unique.user_name()}_{random.randint(1000, 9999)}"
        user = User.objects.create_user(
            username=username,
            email=fake.email(),
            password='password123'
        )
        new_users.append(user)

        resume = Resume.objects.create(
            owner=user,
            success_summary=fake.paragraph(nb_sentences=5)
        )

        # Add Skills
        num_skills = random.randint(3, 8)
        chosen_skills = random.sample(skill_pool, num_skills)
        for skill_name in chosen_skills:
            Skill.objects.create(resume=resume, name=skill_name)

        # Add Education
        num_edu = random.randint(1, 2)
        for _ in range(num_edu):
            Education.objects.create(
                resume=resume,
                school_name=fake.company() + " University",
                degree=random.choice(degrees),
                start_date=fake.date_between(start_date='-10y', end_date='-4y'),
                end_date=fake.date_between(start_date='-4y', end_date='today'),
                description=fake.sentence()
            )

        # Add Previous Jobs
        num_jobs = random.randint(1, 4)
        for _ in range(num_jobs):
            PreviousJob.objects.create(
                resume=resume,
                company=random.choice(companies),
                position=fake.job(),
                start_date=fake.date_between(start_date='-5y', end_date='-1y'),
                end_date=fake.date_between(start_date='-1y', end_date='today'),
                description=fake.paragraph(nb_sentences=3)
            )

    # Generate some ratings for new resumes from existing or new users
    all_users = list(User.objects.all())
    for _ in range(min(len(new_users), 100)):
        rater = random.choice(all_users)
        target_resume = random.choice(Resume.objects.exclude(owner=rater))
        Rating.objects.get_or_create(
            rater=rater,
            resume=target_resume,
            defaults={'score': random.randint(1, 5)}
        )

    return len(new_users)
