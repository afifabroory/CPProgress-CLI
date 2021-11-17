import json
import requests

DATABASE_URL = "https://cp-progress-default-rtdb.asia-southeast1.firebasedatabase.app"
DATABASE_TOKEN = 'THISISVERYVERYSECRETNOBODYKNOW:^)BYTHEWAYTHISISNOTTHETOKENOKAYYOUCANCHANGETHISTOGRANTWRITEACCESSTOREALTIMEDATABASE'

def getData(path='/'):
    return requests.get(DATABASE_URL + path + '.json').json()

def postData(path='/', data={}):
    requests.put(DATABASE_URL + path + '.json?auth=' + DATABASE_TOKEN, data=json.dumps(data))

def isIntegerInput(input):
    try:
        int(input)
        return True
    except ValueError:
        return False

def main():
    cancle = False
    
    submission_id = int(getData('/lastID'))+1
    print("Submission ID\t\t: ", submission_id+1, end="\n\n")
    
    problem_id = ''
    problem_link = ''
    postProblem = False
    while (not cancle):
        problem_id = input("Problem ID\t\t: ").upper()
        if (problem_id == 'q'): 
            cancle = True
            break
        elif (problem_id == ''):
            print("Problem ID cannot be empty")
            continue

        if (getData(path='/problem/' + problem_id) == None):
            print()
            while (True):
                problem_link = input('Problem URL\t\t: ')

                if (problem_link == 'q'): 
                    cancle = True   
                    break
                elif (problem_link == ''):
                    print("Problem URL cannot be empty")
                    continue
                else:
                    postProblem = True
                    break
            break
        else:
            print("Problem ID already exists. Skipped", end="\n\n")
            break

    print()
    
    # AC: Accepted
    # WA: Wrong Answer
    # TLE: Time Limit Exceeded
    # MLE: Memory Limit Exceeded
    # RTE: Runtime Error
    # CTE: Compile Error
    submission_status = ''
    submission_count = 0
    while (not cancle):
        submission_status = input("Submission Status\t: ").upper()
        if (submission_status == 'q'): 
            cancle = True
            break
        elif (submission_status == ''):
            print("Submission Status cannot be empty")
            continue
        elif (submission_status == 'AC' or submission_status == 'WA' 
                or submission_status == 'TLE' or submission_status == 'MLE' 
                or submission_status == 'RTE' or submission_status == 'CTE'):

                # Increate submission count
                submission_count = getData(path='/submissionStatus/overall/' + submission_status)
                submission_count += 1
                break
        else:
            print("Submission Status is not valid")
            continue
    print()

    submission_solution = ''
    while (not cancle):
        submission_solution = input("Solution URL\t\t: ")
        if (submission_solution == 'q'): 
            cancle = True
            break
        elif (submission_solution == ''):
            submission_solution = '-'
            break
        else:
            break
    print()
            
    if (not cancle):
        data = {
            'date': {'.sv': 'timestamp'},
            'problemID': problem_id,
            'status': submission_status,
            'solutionURL': submission_solution
        }
        postData(path='/lastID', data=submission_id)
        postData(path='/submission/' + str(submission_id), data=data)
        postData(path='/submissionStatus/overall/' + submission_status, data=submission_count)

        if (postProblem): postData(path='/problem/'+problem_id, data=problem_link)
    else:
        print('Cancled')


if __name__ == "__main__":
    main()
