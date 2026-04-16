from app.extensions import db
from app.models.job import Job
from app.models.mock_test import MockTest, MockTestQuestion
from app.models.question import Question


def ensure_seed_data():
    if Question.query.count() < 20:
        base_questions = [
            Question(
                company="TCS",
                category="Aptitude",
                difficulty="Easy",
                prompt="If a train travels 120 km in 2 hours, what is the average speed?",
                option_a="50 km/h",
                option_b="60 km/h",
                option_c="70 km/h",
                option_d="80 km/h",
                correct_option="B",
                explanation="Average speed = distance / time = 120 / 2 = 60 km/h.",
            ),
            Question(
                company="Infosys",
                category="Reasoning",
                difficulty="Medium",
                prompt="Find the next number: 2, 6, 12, 20, ?",
                option_a="28",
                option_b="30",
                option_c="32",
                option_d="36",
                correct_option="B",
                explanation="Pattern is n(n+1): 1*2, 2*3, 3*4, 4*5, 5*6.",
            ),
            Question(
                company="Wipro",
                category="Verbal",
                difficulty="Easy",
                prompt="Choose the correctly spelled word.",
                option_a="Accomodation",
                option_b="Acommodation",
                option_c="Accommodation",
                option_d="Accommadation",
                correct_option="C",
                explanation="Accommodation is the correct spelling.",
            ),
            Question(
                company="Accenture",
                category="Programming",
                difficulty="Medium",
                prompt="What is the output of len('HireReady') in Python?",
                option_a="7",
                option_b="8",
                option_c="9",
                option_d="10",
                correct_option="C",
                explanation="HireReady has 9 characters.",
            ),
            Question(
                company="Cognizant",
                category="SQL",
                difficulty="Medium",
                prompt="Which SQL clause is used to filter grouped records?",
                option_a="WHERE",
                option_b="GROUP BY",
                option_c="HAVING",
                option_d="ORDER BY",
                correct_option="C",
                explanation="HAVING filters rows after GROUP BY is applied.",
            ),
            Question(
                company="HCL",
                category="Core",
                difficulty="Hard",
                prompt="In OS, which algorithm may cause starvation?",
                option_a="Round Robin",
                option_b="FCFS",
                option_c="Priority Scheduling",
                option_d="SJF",
                correct_option="C",
                explanation="Strict priority scheduling can starve low-priority processes.",
            ),
        ]

        additional_questions = [
            Question(company="TCS", category="Aptitude", difficulty="Easy", prompt="What is 18% of 250?", option_a="35", option_b="40", option_c="45", option_d="50", correct_option="C", explanation="18% of 250 = 0.18 x 250 = 45."),
            Question(company="Infosys", category="Reasoning", difficulty="Medium", prompt="If all Roses are Flowers and some Flowers fade quickly, which conclusion is always true?", option_a="All roses fade quickly", option_b="Some roses are flowers", option_c="No roses are flowers", option_d="Some flowers are roses", correct_option="B", explanation="From the first statement, every rose is definitely a flower."),
            Question(company="Wipro", category="Verbal", difficulty="Easy", prompt="Choose the antonym of 'Scarce'.", option_a="Rare", option_b="Limited", option_c="Abundant", option_d="Sparse", correct_option="C", explanation="Scarce means insufficient; abundant is the opposite."),
            Question(company="Accenture", category="Programming", difficulty="Medium", prompt="Which Python data type is immutable?", option_a="list", option_b="dict", option_c="set", option_d="tuple", correct_option="D", explanation="Tuple is immutable."),
            Question(company="Cognizant", category="SQL", difficulty="Medium", prompt="Which SQL keyword removes duplicate rows from results?", option_a="UNIQUE", option_b="DISTINCT", option_c="FILTER", option_d="GROUP", correct_option="B", explanation="DISTINCT returns unique rows."),
            Question(company="HCL", category="Core", difficulty="Hard", prompt="Which memory is volatile?", option_a="ROM", option_b="SSD", option_c="RAM", option_d="HDD", correct_option="C", explanation="RAM loses data when power is off."),
            Question(company="TCS", category="Aptitude", difficulty="Easy", prompt="A sum of money doubles in 5 years at simple interest. In how many years will it triple?", option_a="10", option_b="12.5", option_c="15", option_d="20", correct_option="A", explanation="If it doubles in 5 years, interest in 5 years = principal. For triple, interest = 2 x principal, so time = 10 years."),
            Question(company="Infosys", category="Reasoning", difficulty="Medium", prompt="Find the odd one out: 3, 5, 11, 14, 17", option_a="3", option_b="5", option_c="11", option_d="14", correct_option="D", explanation="14 is the only non-prime number."),
            Question(company="Wipro", category="Verbal", difficulty="Easy", prompt="Choose the correct sentence.", option_a="She don't like coffee.", option_b="She doesn't likes coffee.", option_c="She doesn't like coffee.", option_d="She not like coffee.", correct_option="C", explanation="Correct auxiliary usage is 'doesn't like'."),
            Question(company="Accenture", category="Programming", difficulty="Medium", prompt="What does O(log n) indicate?", option_a="Linear growth", option_b="Constant growth", option_c="Logarithmic growth", option_d="Quadratic growth", correct_option="C", explanation="O(log n) means logarithmic time complexity."),
            Question(company="Cognizant", category="SQL", difficulty="Medium", prompt="Which join returns only matching rows from both tables?", option_a="LEFT JOIN", option_b="RIGHT JOIN", option_c="INNER JOIN", option_d="FULL JOIN", correct_option="C", explanation="INNER JOIN returns matched rows only."),
            Question(company="HCL", category="Core", difficulty="Hard", prompt="Which protocol is connection-oriented?", option_a="UDP", option_b="TCP", option_c="ICMP", option_d="ARP", correct_option="B", explanation="TCP establishes and maintains a connection."),
            Question(company="TCS", category="Aptitude", difficulty="Easy", prompt="If a car runs 150 km in 3 hours, its average speed is:", option_a="40 km/h", option_b="45 km/h", option_c="50 km/h", option_d="60 km/h", correct_option="C", explanation="Average speed = distance/time = 150/3 = 50 km/h."),
            Question(company="Infosys", category="Reasoning", difficulty="Medium", prompt="Complete the series: A, C, F, J, O, ?", option_a="T", option_b="U", option_c="V", option_d="W", correct_option="B", explanation="Jumps are +2, +3, +4, +5, so next is +6 -> U."),
        ]

        if Question.query.count() == 0:
            db.session.add_all(base_questions + additional_questions)
        else:
            existing_prompts = {row.prompt for row in Question.query.with_entities(Question.prompt).all()}
            for question in base_questions + additional_questions:
                if question.prompt not in existing_prompts:
                    db.session.add(question)
        db.session.flush()

    if not Job.query.first():
        jobs = [
            Job(company="TCS", role="Graduate Trainee", job_type="Full-time", location="Bengaluru", days_left=5, status="Open"),
            Job(company="Infosys", role="Systems Engineer", job_type="Full-time", location="Hyderabad", days_left=8, status="Open"),
            Job(company="Wipro", role="Project Engineer", job_type="Full-time", location="Chennai", days_left=6, status="Open"),
            Job(company="Accenture", role="Associate Software Engineer", job_type="Full-time", location="Pune", days_left=10, status="Open"),
            Job(company="Cognizant", role="Programmer Analyst", job_type="Full-time", location="Coimbatore", days_left=7, status="Open"),
        ]
        db.session.add_all(jobs)

    selected_questions = Question.query.order_by(Question.id.asc()).limit(20).all()
    if selected_questions:
        test = MockTest.query.order_by(MockTest.id.asc()).first()
        if not test:
            test = MockTest(
                title="Campus Placement Readiness Test",
                company="General",
                duration_minutes=30,
                total_questions=len(selected_questions),
            )
            db.session.add(test)
            db.session.flush()

        existing_links = MockTestQuestion.query.filter_by(mock_test_id=test.id).all()
        existing_question_ids = {link.question_id for link in existing_links}

        if len(existing_links) != len(selected_questions) or not all(question.id in existing_question_ids for question in selected_questions):
            MockTestQuestion.query.filter_by(mock_test_id=test.id).delete()
            links = [
                MockTestQuestion(mock_test_id=test.id, question_id=question.id, position=index + 1)
                for index, question in enumerate(selected_questions)
            ]
            db.session.add_all(links)

        test.total_questions = len(selected_questions)

    db.session.commit()
