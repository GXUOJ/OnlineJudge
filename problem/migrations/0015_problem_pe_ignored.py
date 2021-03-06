# Generated by Django 2.1.7 on 2019-11-16 14:28

from django.db import migrations, models
from django.conf import settings
import os
import json
import hashlib

def update_all_stripped_md5(apps, schema_editor):
    Problem = apps.get_model("problem", "Problem")
    problems = Problem.objects.all()
    for problem in problems:
        test_case_dir = os.path.join(settings.TEST_CASE_DIR, problem.test_case_id)
        try:
            with open(os.path.join(test_case_dir, "info")) as f:
                info = json.load(f)
            if not info["spj"]:
                for id in info["test_cases"]:
                    with open(os.path.join(test_case_dir,f"{id}.out"),"rb") as f:
                        content = f.read()
                        stripped_md5 = hashlib.md5(b"\n".join([x.rstrip() for x in content.split(b"\n") if len(x) > 0])).hexdigest()
                        info["test_cases"][id]["all_stripped_output_md5"] = stripped_md5
                    with open(os.path.join(test_case_dir, "info"), "w", encoding="utf-8") as f:
                        f.write(json.dumps(info, indent=4))
        except Exception as err:
            print(f"{test_case_dir} info not found")


class Migration(migrations.Migration):

    dependencies = [
        ('problem', '0014_problem_share_submission'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='pe_ignored',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(update_all_stripped_md5, reverse_code=migrations.RunPython.noop),
    ]
