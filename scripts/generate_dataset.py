from pathlib import Path
import csv, random

random.seed(42)
ROOT = Path(__file__).resolve().parents[1]
out = ROOT / 'data' / 'internships.csv'

roles = {
'Backend Engineering Intern': ['Python','FastAPI','PostgreSQL','Docker','REST API','Git'],
'Java Backend Intern': ['Java','Spring Boot','PostgreSQL','Docker','REST API','Git'],
'Machine Learning Intern': ['Python','Machine Learning','Pandas','NumPy','Scikit-learn','Git'],
'Data Science Intern': ['Python','Pandas','NumPy','SQL','Scikit-learn','Machine Learning'],
'Frontend Engineering Intern': ['JavaScript','TypeScript','React','Git','REST API'],
'Full Stack Intern': ['JavaScript','React','Node.js','SQL','Docker','Git'],
'Cloud Engineering Intern': ['AWS','Docker','Linux','Git','Python','REST API'],
'DevOps Intern': ['Docker','Kubernetes','AWS','Linux','Git','Python'],
'NLP Intern': ['Python','NLP','Machine Learning','PyTorch','Pandas','NumPy'],
'AI Engineering Intern': ['Python','Machine Learning','PyTorch','FastAPI','Docker','Git'],
'Microservices Intern': ['Java','Spring Boot','Kafka','Docker','Microservices','PostgreSQL'],
'Data Engineering Intern': ['Python','SQL','Pandas','Kafka','AWS','Docker'],
}
companies = ['NovaTech','Vertex Labs','BlueOrbit','Aster Systems','CloudNest','DataForge','PixelWorks','QuantumStack','FinEdge','CodeHarbor','BrightScale','CoreVista']
locations = ['Bengaluru, India','Hyderabad, India','Pune, India','Mumbai, India','Delhi NCR, India','Chennai, India','Remote, India']
rows=[]
for i in range(1,601):
    title, base = random.choice(list(roles.items()))
    skills = list(base)
    extras = random.sample([x for r in roles.values() for x in r if x not in skills], k=random.randint(0,2))
    skills += extras
    company = random.choice(companies)
    remote = random.random() < 0.32
    location = 'Remote, India' if remote else random.choice(locations[:-1])
    exp = random.choice(['0 years','0-1 years','1 year'])
    salary = random.choice(['₹15,000/month','₹20,000/month','₹25,000/month','₹30,000/month',''])
    employment = 'Internship'
    desc = (f"Work with the {company} engineering team on practical {title.lower()} projects. "
            f"You will design, implement, test, and document features using {', '.join(skills[:4])}. "
            f"Collaborate with engineers through Git-based workflows, review code, debug issues, and learn production development practices. "
            f"The internship includes a scoped project, mentorship, and regular technical feedback.")
    rows.append({
      'job_id': f'INT{i:04d}', 'title': title, 'company': company, 'location': location,
      'description': desc, 'skills': ', '.join(dict.fromkeys(skills)), 'experience_required': exp,
      'employment_type': employment, 'salary': salary, 'remote': remote,
      'application_url': f'https://careers.example.com/internships/INT{i:04d}'
    })
with out.open('w', newline='', encoding='utf-8') as f:
    writer=csv.DictWriter(f, fieldnames=rows[0].keys()); writer.writeheader(); writer.writerows(rows)
print(out, len(rows))
