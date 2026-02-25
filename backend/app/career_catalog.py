from __future__ import annotations

from dataclasses import dataclass


CAREER_DEFINITIONS = [
    {
        'name': 'Cybersecurity Specialist',
        'description': 'Protect systems, networks, and data from cyber threats and incidents.',
    },
    {
        'name': 'Data Analyst',
        'description': 'Transform data into insights for better product and business decisions.',
    },
    {
        'name': 'Doctor',
        'description': 'Diagnose and treat patients using medical science and clinical judgment.',
    },
    {
        'name': 'Engineer',
        'description': 'Design and build practical systems, structures, and processes.',
    },
    {
        'name': 'Software Developer',
        'description': 'Build and maintain software systems for web, mobile, and cloud platforms.',
    },
]

SKILL_AREA_DEFINITIONS = [
    {
        'name': 'Programming',
        'description': 'Write maintainable code, debug issues, and implement features effectively.',
        'importance_level': 'critical',
    },
    {
        'name': 'Data Structures',
        'description': 'Use the right in-memory data structures to improve runtime and reliability.',
        'importance_level': 'critical',
    },
    {
        'name': 'Algorithms',
        'description': 'Design efficient algorithmic solutions and reason about complexity.',
        'importance_level': 'high',
    },
    {
        'name': 'System Design',
        'description': 'Design scalable software architectures and service boundaries.',
        'importance_level': 'high',
    },
    {
        'name': 'Databases',
        'description': 'Model data and optimize storage, indexing, and query performance.',
        'importance_level': 'high',
    },
    {
        'name': 'Statistics',
        'description': 'Apply statistical methods to quantify uncertainty and validate findings.',
        'importance_level': 'critical',
    },
    {
        'name': 'SQL',
        'description': 'Query relational data with joins, aggregations, and window functions.',
        'importance_level': 'high',
    },
    {
        'name': 'Data Visualization',
        'description': 'Communicate insights with clear charts, dashboards, and storytelling.',
        'importance_level': 'high',
    },
    {
        'name': 'Python Programming',
        'description': 'Use Python tools and libraries for analysis, automation, and modeling.',
        'importance_level': 'high',
    },
    {
        'name': 'Business Analysis',
        'description': 'Frame business questions and translate analysis into stakeholder action.',
        'importance_level': 'moderate',
    },
    {
        'name': 'Network Security',
        'description': 'Secure networks through segmentation, monitoring, and hardening.',
        'importance_level': 'critical',
    },
    {
        'name': 'Threat Analysis',
        'description': 'Identify attack patterns and assess risk in changing threat landscapes.',
        'importance_level': 'high',
    },
    {
        'name': 'Cryptography',
        'description': 'Understand encryption, hashing, and PKI for secure data handling.',
        'importance_level': 'high',
    },
    {
        'name': 'Incident Response',
        'description': 'Detect, contain, and recover from security incidents quickly.',
        'importance_level': 'critical',
    },
    {
        'name': 'Ethical Hacking',
        'description': 'Assess system vulnerabilities using offensive security techniques.',
        'importance_level': 'high',
    },
    {
        'name': 'Biology',
        'description': 'Understand biological systems relevant to patient health.',
        'importance_level': 'critical',
    },
    {
        'name': 'Anatomy',
        'description': 'Learn human body structure for diagnosis and treatment planning.',
        'importance_level': 'critical',
    },
    {
        'name': 'Patient Care',
        'description': 'Deliver safe and empathetic care in clinical environments.',
        'importance_level': 'high',
    },
    {
        'name': 'Medical Diagnostics',
        'description': 'Interpret tests and symptoms to build differential diagnoses.',
        'importance_level': 'critical',
    },
    {
        'name': 'Pharmacology',
        'description': 'Understand drug interactions, dosing, and treatment protocols.',
        'importance_level': 'high',
    },
    {
        'name': 'Mathematics',
        'description': 'Apply quantitative reasoning to solve engineering problems.',
        'importance_level': 'critical',
    },
    {
        'name': 'Physics',
        'description': 'Use mechanics, electricity, and materials principles in design.',
        'importance_level': 'high',
    },
    {
        'name': 'CAD Design',
        'description': 'Model and prototype components using computer-aided design tools.',
        'importance_level': 'high',
    },
    {
        'name': 'Project Management',
        'description': 'Plan scope, timelines, and risks to deliver engineering projects.',
        'importance_level': 'moderate',
    },
    {
        'name': 'Materials Science',
        'description': 'Select and evaluate materials for performance and safety.',
        'importance_level': 'high',
    },
]

CAREER_TO_SKILLS = {
    'Software Developer': ['Programming', 'Data Structures', 'Algorithms', 'System Design', 'Databases'],
    'Data Analyst': ['Statistics', 'SQL', 'Data Visualization', 'Python Programming', 'Business Analysis'],
    'Cybersecurity Specialist': ['Network Security', 'Threat Analysis', 'Cryptography', 'Incident Response', 'Ethical Hacking'],
    'Doctor': ['Biology', 'Anatomy', 'Patient Care', 'Medical Diagnostics', 'Pharmacology'],
    'Engineer': ['Mathematics', 'Physics', 'CAD Design', 'Project Management', 'Materials Science'],
}

SUBJECT_DEFINITIONS = [
    {
        'name': 'Computer Science',
        'field_of_study': 'Computer Science',
        'description': 'Core computing principles, abstraction, and software systems.',
    },
    {
        'name': 'Software Development',
        'field_of_study': 'Computer Science',
        'description': 'Software lifecycle, design patterns, and production delivery.',
    },
    {
        'name': 'Introduction to Programming',
        'field_of_study': 'Computer Science',
        'description': 'Programming fundamentals, control flow, and problem decomposition.',
    },
    {
        'name': 'Object-Oriented Programming',
        'field_of_study': 'Computer Science',
        'description': 'Classes, inheritance, polymorphism, and maintainable code structures.',
    },
    {
        'name': 'Data Structures and Algorithms',
        'field_of_study': 'Computer Science',
        'description': 'Foundational algorithms and data structures for efficient software.',
    },
    {
        'name': 'Database Systems',
        'field_of_study': 'Computer Science',
        'description': 'Relational modeling, normalization, indexing, and transaction concepts.',
    },
    {
        'name': 'Statistics',
        'field_of_study': 'General',
        'description': 'Descriptive and inferential techniques for decision making.',
    },
    {
        'name': 'Data Analysis',
        'field_of_study': 'Data Science',
        'description': 'Data cleaning, transformation, exploratory analysis, and interpretation.',
    },
    {
        'name': 'Probability Theory',
        'field_of_study': 'General',
        'description': 'Probabilistic modeling and uncertainty estimation techniques.',
    },
    {
        'name': 'Business Intelligence',
        'field_of_study': 'Business',
        'description': 'Decision support, KPI tracking, and dashboard-driven communication.',
    },
    {
        'name': 'Information Security',
        'field_of_study': 'Computer Science',
        'description': 'Security principles, secure coding, and system hardening practices.',
    },
    {
        'name': 'Computer Networks',
        'field_of_study': 'Computer Science',
        'description': 'Network architecture, routing, protocols, and performance analysis.',
    },
    {
        'name': 'Digital Forensics',
        'field_of_study': 'Computer Science',
        'description': 'Investigative methods for incident analysis and evidence handling.',
    },
    {
        'name': 'Biology',
        'field_of_study': 'Medicine',
        'description': 'Cell biology, physiology, and biological system fundamentals.',
    },
    {
        'name': 'Human Anatomy',
        'field_of_study': 'Medicine',
        'description': 'Human body systems and structural relationships in healthcare.',
    },
    {
        'name': 'Clinical Medicine',
        'field_of_study': 'Medicine',
        'description': 'Diagnostic reasoning, patient examination, and treatment planning.',
    },
    {
        'name': 'Pharmacology',
        'field_of_study': 'Medicine',
        'description': 'Drug mechanisms, interactions, adverse effects, and therapeutics.',
    },
    {
        'name': 'Calculus',
        'field_of_study': 'Engineering',
        'description': 'Differential and integral calculus for modeling change and systems.',
    },
    {
        'name': 'Engineering Physics',
        'field_of_study': 'Engineering',
        'description': 'Applied mechanics, waves, thermodynamics, and electromagnetism.',
    },
    {
        'name': 'Engineering Design',
        'field_of_study': 'Engineering',
        'description': 'Design process, prototyping, constraint analysis, and verification.',
    },
    {
        'name': 'Materials Engineering',
        'field_of_study': 'Engineering',
        'description': 'Material properties, failure analysis, and selection tradeoffs.',
    },
    {
        'name': 'Project Planning',
        'field_of_study': 'Engineering',
        'description': 'Scheduling, risk planning, and cost-aware project execution.',
    },
]

SKILL_TO_SUBJECTS = {
    'Programming': [
        ('Computer Science', 'high'),
        ('Software Development', 'critical'),
        ('Introduction to Programming', 'critical'),
        ('Object-Oriented Programming', 'high'),
    ],
    'Data Structures': [('Data Structures and Algorithms', 'critical'), ('Computer Science', 'high')],
    'Algorithms': [('Data Structures and Algorithms', 'critical'), ('Calculus', 'moderate')],
    'System Design': [('Software Development', 'high'), ('Database Systems', 'high')],
    'Databases': [('Database Systems', 'critical'), ('Data Analysis', 'moderate')],
    'Statistics': [('Statistics', 'critical'), ('Probability Theory', 'high'), ('Data Analysis', 'high')],
    'SQL': [('Database Systems', 'critical'), ('Data Analysis', 'high')],
    'Data Visualization': [('Data Analysis', 'high'), ('Business Intelligence', 'critical')],
    'Python Programming': [('Introduction to Programming', 'high'), ('Data Analysis', 'high')],
    'Business Analysis': [('Business Intelligence', 'critical'), ('Statistics', 'moderate')],
    'Network Security': [('Information Security', 'critical'), ('Computer Networks', 'high')],
    'Threat Analysis': [('Information Security', 'high'), ('Digital Forensics', 'critical')],
    'Cryptography': [('Information Security', 'critical'), ('Calculus', 'moderate')],
    'Incident Response': [('Digital Forensics', 'critical'), ('Computer Networks', 'moderate')],
    'Ethical Hacking': [('Information Security', 'critical'), ('Computer Networks', 'high')],
    'Biology': [('Biology', 'critical')],
    'Anatomy': [('Human Anatomy', 'critical')],
    'Patient Care': [('Clinical Medicine', 'critical')],
    'Medical Diagnostics': [('Clinical Medicine', 'critical'), ('Biology', 'moderate')],
    'Pharmacology': [('Pharmacology', 'critical')],
    'Mathematics': [('Calculus', 'critical'), ('Engineering Physics', 'high')],
    'Physics': [('Engineering Physics', 'critical')],
    'CAD Design': [('Engineering Design', 'critical')],
    'Project Management': [('Project Planning', 'critical')],
    'Materials Science': [('Materials Engineering', 'critical')],
}

SUBJECT_RESOURCES = {
    'Computer Science': [
        {
            'title': 'Harvard CS50',
            'url': 'https://cs50.harvard.edu/x/',
            'provider': 'Harvard',
        },
        {
            'title': 'Teach Yourself CS Guide',
            'url': 'https://teachyourselfcs.com/',
            'provider': 'Open Guide',
        },
    ],
    'Software Development': [
        {
            'title': 'Software Design and Architecture',
            'url': 'https://www.coursera.org/specializations/software-design-architecture',
            'provider': 'Coursera',
        },
        {
            'title': 'System Design Primer',
            'url': 'https://github.com/donnemartin/system-design-primer',
            'provider': 'GitHub',
        },
    ],
    'Introduction to Programming': [
        {
            'title': 'Python for Everybody',
            'url': 'https://www.py4e.com/',
            'provider': 'PY4E',
        },
        {
            'title': 'Khan Academy Intro to JS',
            'url': 'https://www.khanacademy.org/computing/computer-programming',
            'provider': 'Khan Academy',
        },
    ],
    'Object-Oriented Programming': [
        {
            'title': 'Object Oriented Programming in Java',
            'url': 'https://www.coursera.org/specializations/object-oriented-programming',
            'provider': 'Coursera',
        },
        {
            'title': 'Refactoring Guru',
            'url': 'https://refactoring.guru/',
            'provider': 'Refactoring Guru',
        },
    ],
    'Data Structures and Algorithms': [
        {
            'title': 'NeetCode Practice Roadmap',
            'url': 'https://neetcode.io/roadmap',
            'provider': 'NeetCode',
        },
        {
            'title': 'MIT 6.006 OpenCourseWare',
            'url': 'https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/',
            'provider': 'MIT OpenCourseWare',
        },
    ],
    'Database Systems': [
        {
            'title': 'Mode SQL Tutorial',
            'url': 'https://mode.com/sql-tutorial/',
            'provider': 'Mode',
        },
        {
            'title': 'Stanford Databases',
            'url': 'https://online.stanford.edu/courses/soe-ydbsdatabases-databases',
            'provider': 'Stanford Online',
        },
    ],
    'Statistics': [
        {
            'title': 'Khan Academy Statistics and Probability',
            'url': 'https://www.khanacademy.org/math/statistics-probability',
            'provider': 'Khan Academy',
        },
        {
            'title': 'OpenIntro Statistics',
            'url': 'https://www.openintro.org/book/os/',
            'provider': 'OpenIntro',
        },
    ],
    'Data Analysis': [
        {
            'title': 'Google Data Analytics Certificate',
            'url': 'https://www.coursera.org/professional-certificates/google-data-analytics',
            'provider': 'Coursera',
        },
        {
            'title': 'Kaggle Learn',
            'url': 'https://www.kaggle.com/learn',
            'provider': 'Kaggle',
        },
    ],
    'Probability Theory': [
        {
            'title': 'MIT Probability Course',
            'url': 'https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2014/',
            'provider': 'MIT OpenCourseWare',
        },
        {
            'title': 'Brilliant Probability',
            'url': 'https://brilliant.org/courses/probability/',
            'provider': 'Brilliant',
        },
    ],
    'Business Intelligence': [
        {
            'title': 'Microsoft Power BI Learning',
            'url': 'https://learn.microsoft.com/en-us/training/powerplatform/power-bi/',
            'provider': 'Microsoft Learn',
        },
        {
            'title': 'Tableau Public Training',
            'url': 'https://public.tableau.com/app/learn/training',
            'provider': 'Tableau',
        },
    ],
    'Information Security': [
        {
            'title': 'Intro to Cybersecurity',
            'url': 'https://www.netacad.com/courses/cybersecurity/introduction-cybersecurity',
            'provider': 'Cisco Networking Academy',
        },
        {
            'title': 'OWASP Top 10',
            'url': 'https://owasp.org/www-project-top-ten/',
            'provider': 'OWASP',
        },
    ],
    'Computer Networks': [
        {
            'title': 'Computer Networking Course',
            'url': 'https://www.geeksforgeeks.org/computer-network-tutorials/',
            'provider': 'GeeksforGeeks',
        },
        {
            'title': 'Stanford Networking',
            'url': 'https://online.stanford.edu/courses/soe-ycs0007-computer-networking',
            'provider': 'Stanford Online',
        },
    ],
    'Digital Forensics': [
        {
            'title': 'SANS Digital Forensics Posters',
            'url': 'https://www.sans.org/posters/',
            'provider': 'SANS',
        },
        {
            'title': 'DFIR Training Repository',
            'url': 'https://www.dfir.training/',
            'provider': 'DFIR Training',
        },
    ],
    'Biology': [
        {
            'title': 'Khan Academy Biology',
            'url': 'https://www.khanacademy.org/science/biology',
            'provider': 'Khan Academy',
        },
        {
            'title': 'OpenStax Biology',
            'url': 'https://openstax.org/details/books/biology-2e',
            'provider': 'OpenStax',
        },
    ],
    'Human Anatomy': [
        {
            'title': 'AnatomyZone',
            'url': 'https://anatomyzone.com/',
            'provider': 'AnatomyZone',
        },
        {
            'title': 'TeachMeAnatomy',
            'url': 'https://teachmeanatomy.info/',
            'provider': 'TeachMeSeries',
        },
    ],
    'Clinical Medicine': [
        {
            'title': 'NICE Clinical Knowledge Summaries',
            'url': 'https://cks.nice.org.uk/',
            'provider': 'NICE',
        },
        {
            'title': 'AMBOSS Learning Cards',
            'url': 'https://www.amboss.com/us/knowledge',
            'provider': 'AMBOSS',
        },
    ],
    'Pharmacology': [
        {
            'title': 'Pharmacology by Osmosis',
            'url': 'https://www.osmosis.org/learn/Pharmacology',
            'provider': 'Osmosis',
        },
        {
            'title': 'Open Pharmacology Notes',
            'url': 'https://pressbooks.umn.edu/pharmacology/',
            'provider': 'Open Textbook',
        },
    ],
    'Calculus': [
        {
            'title': 'Khan Academy Calculus',
            'url': 'https://www.khanacademy.org/math/calculus-1',
            'provider': 'Khan Academy',
        },
        {
            'title': 'MIT Single Variable Calculus',
            'url': 'https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/',
            'provider': 'MIT OpenCourseWare',
        },
    ],
    'Engineering Physics': [
        {
            'title': 'MIT Physics I',
            'url': 'https://ocw.mit.edu/courses/8-01sc-classical-mechanics-fall-2016/',
            'provider': 'MIT OpenCourseWare',
        },
        {
            'title': 'The Engineering Mindset Physics',
            'url': 'https://theengineeringmindset.com/category/physics/',
            'provider': 'The Engineering Mindset',
        },
    ],
    'Engineering Design': [
        {
            'title': 'Autodesk Design Academy',
            'url': 'https://www.autodesk.com/education/edu-software/overview',
            'provider': 'Autodesk',
        },
        {
            'title': 'SolidWorks Tutorials',
            'url': 'https://my.solidworks.com/training',
            'provider': 'SolidWorks',
        },
    ],
    'Materials Engineering': [
        {
            'title': 'Introduction to Materials Science',
            'url': 'https://ocw.mit.edu/courses/3-091sc-introduction-to-solid-state-chemistry-fall-2010/',
            'provider': 'MIT OpenCourseWare',
        },
        {
            'title': 'Materials Project',
            'url': 'https://materialsproject.org/',
            'provider': 'Materials Project',
        },
    ],
    'Project Planning': [
        {
            'title': 'Google Project Management',
            'url': 'https://www.coursera.org/professional-certificates/google-project-management',
            'provider': 'Coursera',
        },
        {
            'title': 'PMI Fundamentals',
            'url': 'https://www.pmi.org/learning/training-development',
            'provider': 'PMI',
        },
    ],
}


@dataclass(frozen=True)
class SkillMetricRule:
    metric_name: str
    higher_is_better: bool
    weight: float


SKILL_METRIC_RULES: dict[str, list[SkillMetricRule]] = {
    'Programming': [
        SkillMetricRule('study_hours', True, 0.3),
        SkillMetricRule('focus_score', True, 0.3),
        SkillMetricRule('assignments_completed_per_week', True, 0.25),
        SkillMetricRule('phone_usage_hours', False, 0.15),
    ],
    'Data Structures': [
        SkillMetricRule('focus_score', True, 0.35),
        SkillMetricRule('study_hours', True, 0.35),
        SkillMetricRule('sleep_hours', True, 0.15),
        SkillMetricRule('stress_level', False, 0.15),
    ],
    'Algorithms': [
        SkillMetricRule('focus_score', True, 0.35),
        SkillMetricRule('study_hours', True, 0.3),
        SkillMetricRule('sleep_hours', True, 0.2),
        SkillMetricRule('stress_level', False, 0.15),
    ],
    'System Design': [
        SkillMetricRule('study_hours', True, 0.35),
        SkillMetricRule('focus_score', True, 0.25),
        SkillMetricRule('breaks_per_day', True, 0.15),
        SkillMetricRule('social_media_hours', False, 0.25),
    ],
    'Databases': [
        SkillMetricRule('study_hours', True, 0.35),
        SkillMetricRule('assignments_completed_per_week', True, 0.3),
        SkillMetricRule('focus_score', True, 0.2),
        SkillMetricRule('phone_usage_hours', False, 0.15),
    ],
    'Statistics': [
        SkillMetricRule('study_hours', True, 0.35),
        SkillMetricRule('focus_score', True, 0.3),
        SkillMetricRule('sleep_hours', True, 0.15),
        SkillMetricRule('stress_level', False, 0.2),
    ],
    'SQL': [
        SkillMetricRule('study_hours', True, 0.35),
        SkillMetricRule('assignments_completed_per_week', True, 0.3),
        SkillMetricRule('focus_score', True, 0.2),
        SkillMetricRule('phone_usage_hours', False, 0.15),
    ],
    'Data Visualization': [
        SkillMetricRule('focus_score', True, 0.3),
        SkillMetricRule('study_hours', True, 0.3),
        SkillMetricRule('sleep_hours', True, 0.15),
        SkillMetricRule('social_media_hours', False, 0.25),
    ],
    'Python Programming': [
        SkillMetricRule('study_hours', True, 0.35),
        SkillMetricRule('focus_score', True, 0.3),
        SkillMetricRule('assignments_completed_per_week', True, 0.2),
        SkillMetricRule('gaming_hours', False, 0.15),
    ],
    'Business Analysis': [
        SkillMetricRule('focus_score', True, 0.35),
        SkillMetricRule('study_hours', True, 0.2),
        SkillMetricRule('attendance_percentage', True, 0.25),
        SkillMetricRule('stress_level', False, 0.2),
    ],
    'Network Security': [
        SkillMetricRule('study_hours', True, 0.35),
        SkillMetricRule('focus_score', True, 0.25),
        SkillMetricRule('sleep_hours', True, 0.15),
        SkillMetricRule('stress_level', False, 0.25),
    ],
    'Threat Analysis': [
        SkillMetricRule('focus_score', True, 0.35),
        SkillMetricRule('study_hours', True, 0.25),
        SkillMetricRule('sleep_hours', True, 0.15),
        SkillMetricRule('phone_usage_hours', False, 0.25),
    ],
    'Cryptography': [
        SkillMetricRule('study_hours', True, 0.35),
        SkillMetricRule('focus_score', True, 0.35),
        SkillMetricRule('stress_level', False, 0.2),
        SkillMetricRule('sleep_hours', True, 0.1),
    ],
    'Incident Response': [
        SkillMetricRule('focus_score', True, 0.3),
        SkillMetricRule('sleep_hours', True, 0.25),
        SkillMetricRule('stress_level', False, 0.25),
        SkillMetricRule('study_hours', True, 0.2),
    ],
    'Ethical Hacking': [
        SkillMetricRule('study_hours', True, 0.3),
        SkillMetricRule('focus_score', True, 0.3),
        SkillMetricRule('social_media_hours', False, 0.2),
        SkillMetricRule('gaming_hours', False, 0.2),
    ],
    'Biology': [
        SkillMetricRule('study_hours', True, 0.35),
        SkillMetricRule('attendance_percentage', True, 0.25),
        SkillMetricRule('sleep_hours', True, 0.2),
        SkillMetricRule('stress_level', False, 0.2),
    ],
    'Anatomy': [
        SkillMetricRule('study_hours', True, 0.4),
        SkillMetricRule('focus_score', True, 0.3),
        SkillMetricRule('attendance_percentage', True, 0.2),
        SkillMetricRule('stress_level', False, 0.1),
    ],
    'Patient Care': [
        SkillMetricRule('attendance_percentage', True, 0.35),
        SkillMetricRule('sleep_hours', True, 0.2),
        SkillMetricRule('stress_level', False, 0.25),
        SkillMetricRule('focus_score', True, 0.2),
    ],
    'Medical Diagnostics': [
        SkillMetricRule('focus_score', True, 0.35),
        SkillMetricRule('study_hours', True, 0.25),
        SkillMetricRule('sleep_hours', True, 0.2),
        SkillMetricRule('stress_level', False, 0.2),
    ],
    'Pharmacology': [
        SkillMetricRule('study_hours', True, 0.35),
        SkillMetricRule('focus_score', True, 0.25),
        SkillMetricRule('attendance_percentage', True, 0.25),
        SkillMetricRule('phone_usage_hours', False, 0.15),
    ],
    'Mathematics': [
        SkillMetricRule('focus_score', True, 0.35),
        SkillMetricRule('study_hours', True, 0.3),
        SkillMetricRule('assignments_completed_per_week', True, 0.2),
        SkillMetricRule('social_media_hours', False, 0.15),
    ],
    'Physics': [
        SkillMetricRule('study_hours', True, 0.35),
        SkillMetricRule('focus_score', True, 0.3),
        SkillMetricRule('sleep_hours', True, 0.15),
        SkillMetricRule('stress_level', False, 0.2),
    ],
    'CAD Design': [
        SkillMetricRule('study_hours', True, 0.35),
        SkillMetricRule('focus_score', True, 0.25),
        SkillMetricRule('assignments_completed_per_week', True, 0.2),
        SkillMetricRule('phone_usage_hours', False, 0.2),
    ],
    'Project Management': [
        SkillMetricRule('attendance_percentage', True, 0.3),
        SkillMetricRule('breaks_per_day', True, 0.2),
        SkillMetricRule('stress_level', False, 0.3),
        SkillMetricRule('focus_score', True, 0.2),
    ],
    'Materials Science': [
        SkillMetricRule('study_hours', True, 0.3),
        SkillMetricRule('focus_score', True, 0.3),
        SkillMetricRule('sleep_hours', True, 0.2),
        SkillMetricRule('assignments_completed_per_week', True, 0.2),
    ],
}


def slugify_name(name: str) -> str:
    return '-'.join(name.strip().lower().split())
