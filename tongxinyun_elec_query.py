import requests
import json
from pprint import pprint
import sys
import getopt

# open_token lies in EMP_SHELL_SP_KEY.xml, name=openToken
# user_id lies in EMP_SHELL_SP_KEY.xml, name=last_login_user_name or else


def get_tongxinyun_elec_ticket(user_id: str, open_token: str) -> str:
    # Step 1
    # from your openToken and userId get your login ticket
    step_one_headers = {
        'openToken': open_token,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'tjyun.tongji.edu.cn',
        'Connection': 'close',
    }
    step_one_base_url = "http://tjyun.tongji.edu.cn/3gol/getLightAppURL.action"
    step_one_url = step_one_base_url + "?openToken="
    step_one_url += open_token
    step_one_url += "&appid=200019&mid=104"
    step_one_url += "&userId="
    step_one_url += user_id
    step_one_url += "&urlParam=https%3A%2F%2Ftjpay.tongji.edu.cn%2F%23%2FHomePage"
    temp = requests.post(step_one_url, headers=step_one_headers)
    temp_json_result = json.loads(temp.text)
    # get your ticket!
    elec_ticket = temp_json_result['data']['ticket']
    # put temp_json_result['data']['url'] in your browser to directly login into it.
    return elec_ticket


def get_tongjixun_elec_jwt(elec_ticket: str) -> [str, str]:
    # Step two
    # Login and get JWT
    step_two_headers = {
        'Host': 'tjpay.tongji.edu.cn:8080',
        'Referer': 'tjpay.tongji.edu.cn:8080',
        'X-Requested-With': 'com.tongjidaxue.kdweibo.client',
        'Connection': 'close',
    }
    step_two_url = "https://tjpay.tongji.edu.cn:8080/user/login"
    # if don't use tuple, requests will adds "filename" tag to the multi-form data body
    params = {
        "ticket": (None, elec_ticket)
    }
    temp = requests.post(step_two_url, headers=step_two_headers, files=params)
    # verify your result here.
    # print(temp.request.body.decode('utf-8'))
    temp_json_result = json.loads(temp.text)
    elec_userid = temp_json_result['data']['userId']
    response_headers = temp.headers
    # 'Authorization': 'Bearer ******'
    auth_jwt = response_headers['Authorization']
    return auth_jwt, elec_userid


def get_tongxinyun_elec(auth_jwt: str, elec_userid: str) -> str:
    # Step three
    step_three_headers = {
        'Origin': 'https://tjpay.tongji.edu.cn',
        'Authorization': auth_jwt,
        'X-Requested-With': 'com.tongjidaxue.kdweibo.client',
        'Connection': 'close',
    }
    step_three_base_url = "https://tjpay.tongji.edu.cn:8080/user/merchant/elec/dorms/list"
    step_three_url = step_three_base_url + "?userId="
    step_three_url += elec_userid
    temp = requests.get(step_three_url, headers=step_three_headers)
    temp_json_result = json.loads(temp.text)
    return temp_json_result


def tongxinyun_elec_query(user_id: str, open_token: str) -> dict:
    ticket = get_tongxinyun_elec_ticket(user_id, open_token)
    auth_jwt, elec_userid = get_tongjixun_elec_jwt(ticket)
    result = get_tongxinyun_elec(auth_jwt, elec_userid)
    return result


def show_help():
    print('Usage: tongxinyun_elec_query.py -o <openToken> -u <userId>')
    print('   or: tongxinyun_elec_query.py --openToken=<openToken> --userId=<userId>')
    print('You should get your openToken and userId from Tongxinyun.')


def main(argv):
    _openToken = ""
    _userId = ""
    try:
        opts, args = getopt.getopt(
            argv, "ho:u:", ["help", "openToken=", "userId="])
    except getopt.GetoptError:
        show_help()
        exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_help()
            sys.exit(1)
        elif opt in ("-o", "--openToken"):
            _openToken = arg
        elif opt in ("-u", "--userId"):
            _userId = arg

    if _openToken == "" or _userId == "":
        print("Missing options.")
        show_help()
        exit(3)

    result = tongxinyun_elec_query(_userId, _openToken)
    try:
        result_data = result['data']
        for data in result_data:
            print(data['building'] + data['room'] + ": " + str(data['remain']))
    except KeyError:
        print("There maybe something wrong on Tongxinyun's side. Try again later.")
    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
