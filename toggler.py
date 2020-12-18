import requests
import pprint
import json
from requests.auth import HTTPBasicAuth
import datetime
from datetime import datetime as dt
import sys
import csv
from zoneinfo import ZoneInfo
from argparse import ArgumentParser

def get_workspace_id(api_token):
    r = requests.get('https://www.toggl.com/api/v8/workspaces',
                     auth=(api_token, 'api_token'))

    data = r.json()
    Data = data[0]
    return Data['id']


def get_projects(api_token, workspace_id):
    p_dictionary = {}
    r = requests.get('https://www.toggl.com/api/v8/workspaces/{0}/projects'.format(workspace_id),
                     auth=(api_token, 'api_token'))

    data = r.json()
    for d in data:
        p_dictionary[d["name"]] = d["id"]
    pprint.pprint(p_dictionary)


def post_entries(api_token, bill, project_id, duration, start):
    params = {
        "time_entry": {
            "billable": bill,
            "duration": duration,
            "start": start,
            "pid": project_id,
            "created_with": "app"
        }
    }
    res = requests.post('https://www.toggl.com/api/v8/time_entries',
                        auth=HTTPBasicAuth(api_token, 'api_token'),
                        headers={'Content-Type': 'application/json'},
                        data=json.dumps(params))
    print(res.status_code)


def get_records(akashi_token, company_id, start_date, end_date):
    params = {
        'token': akashi_token,
        'start_date': start_date,
        'end_date': end_date
    }
    res = requests.get('https://atnd.ak4.jp/api/cooperation/{0}/stamps'.format(company_id),
                       params)

    print(res.status_code)
    l_time = [dt.strptime(d.get('stamped_at'), '%Y/%m/%d %H:%M:%S').replace(
        tzinfo=ZoneInfo("Asia/Tokyo")) for d in res.json()['response']['stamps']]
    pprint.pprint(l_time)
    times = []
    for i in range(len(l_time)-1):
        a = [item for item in times if l_time[i] in item]
        if l_time[i].date() == l_time[i+1].date() and not a:
            times.append((l_time[i], l_time[i+1]))
    pprint.pprint(times)

    return times


def toggle_oneday(day, start, end, work_id, token):
    lt_start = day + datetime.timedelta(hours=13)
    lt_end = day + datetime.timedelta(hours=14)
    dur1 = lt_start - start
    dur2 = end - lt_end
    post_entries(token, True, work_id, dur1.seconds, start.isoformat())
    post_entries(token, False, break_project_id, 3600, lt_start.isoformat())
    post_entries(token, True, work_id, dur2.seconds, lt_end.isoformat())


def toggle_with_csv():
    tokyo = ZoneInfo("Asia/Tokyo")
    with open("dates.csv") as f:
        reader = csv.reader(f)
        for l in reader:
            day = dt.strptime(
                l[0], '%Y-%m-%d').replace(tzinfo=tokyo)
            start = dt.strptime(
                l[0]+l[1], '%Y-%m-%d%H:%M').replace(tzinfo=tokyo)
            end = dt.strptime(
                l[0]+l[2], '%Y-%m-%d%H:%M').replace(tzinfo=tokyo)
            toggle_oneday(day, start, end, hox002, toggl_token)


def toggle_with_akashiApi(start, end):
    times = get_records(akashi_token, company_id, start, end)

    for i in times:
        toggle_oneday(dt(
            i[0].year, i[0].month, i[0].day).replace(tzinfo=ZoneInfo("Asia/Tokyo")), i[0], i[1], working_project_id, toggl_token)


def get_option():
    argparser = ArgumentParser()
    argparser.add_argument('-t', '--togglToken', type=str,
                           default=toggl_token,
                           help='Toggl Token')
    argparser.add_argument('-a', '--akashiToken', type=str,
                           default=akashi_token,
                           help='Akashi Token')
    argparser.add_argument('-wid', '--workspaceId', type=int,
                           default=workspace_id,
                           help='Workspace Id.')
    argparser.add_argument('-b', '--breakNumber', type=int,
                           default=break_project_id,
                           help='Project number of break time.')
    argparser.add_argument('-pid', '--workingProjectId', type=int,
                           default=working_project_id,
                           help='Working Project Number.')
    argparser.add_argument('-c', '--companyId', type=str,
                           default=company_id,
                           help='Company Id.')
    argparser.add_argument('-s', '--start', type=int,
                           default=start,
                           help='Start Date for auto inputting.')
    argparser.add_argument('-e', '--end', type=str,
                           default=end,
                           help='End Date for auto inputting.')
    return argparser.parse_args()

def save_command_log():
    f = open("logs/command-log-{}.txt".format(dt.now().strftime("%Y-%m-%d_%H:%M:%S")),'a')
    f.write('python3 ' + ' '.join(sys.argv) + '\n')
    f.close()

if __name__ == '__main__':
    toggl_token = 'token'
    akashi_token = 'token'
    workspace_id = 0000000
    break_project_id = 00000000
    working_project_id = 00000000
    company_id = "companyid"
    start = 20201210000000
    end = 20201220000000
    #yyyyMMddHHmmss   

    args = get_option()

    toggl_token = args.togglToken
    akashi_token = args.akashiToken
    workspace_id = args.workspaceId
    break_project_id = args.breakNumber
    working_project_id = args.workingProjectId
    company_id = args.companyId
    start = args.start
    end = args.end
    #workspace_id = get_workspace_id(toggl_token)
    #get_projects(toggl_token, workspace_id)
    toggle_with_akashiApi(start, end)
    save_command_log()
