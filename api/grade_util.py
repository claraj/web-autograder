from datetime import datetime
import json


def generate_github_url(grade):
    if not grade.assignment or not grade.student:
        return
    url = 'https://github.com/%s/%s-%s' % ( grade.assignment.github_org , grade.assignment.github_base , grade.student.github_id)
    return url


def is_same_commit(one, another):
    return one.github_commit_hash == another.github_commit_hash


def is_same_ag_error(one, another):
    return (one.ag_error == another.ag_error)


def bring_comments_forward(new_grade, previous):

    timestamp = get_timestring_prefix(previous.date)

    prev_rep = json.loads(previous.generated_report)
    new_rep = json.loads(new_grade.generated_report)

    # If the previous run errored, there will be no question reports
    if not 'question_reports' in prev_rep:
        return

    # If the previous run worked but this one failed, then 

    prev_questions = prev_rep['question_reports']
    new_questions = new_rep['question_reports']

    for (pq, nq) in zip(prev_questions, new_questions):
        if 'adjusted_points' in pq:
            nq['adjusted_points'] = pq['adjusted_points']
        if 'instructor_comments' in pq:
            comments = pq['instructor_comments']
            already_date = re.match(r'^\d\d/\d\d/\d\d', comments)
            if already_date:
                nq['instructor_comments'] = pq['instructor_comments']
            else:
                nq['instructor_comments'] = timestamp + pq['instructor_comments']

    if 'overall_instructor_comments' in prev_rep:

        comments = prev_rep['overall_instructor_comments']
        # does this start with a date?
        already_date = re.match(r'^\d\d/\d\d/\d\d', comments)
        if already_date:
            new_rep['overall_instructor_comments'] = prev_rep['overall_instructor_comments']
        else:
            new_rep['overall_instructor_comments'] = timestamp + prev_rep['overall_instructor_comments']

    return json.dumps(new_rep)


def get_timestring_prefix(date):
    return date.strftime('%m/%d/%y %H:%M ')   # 12/31/18 16:30
