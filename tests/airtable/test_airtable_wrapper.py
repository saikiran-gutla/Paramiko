from airtable import Airtable
import pytest


@pytest.mark.xfail(run=False)
def test_airtable():
    airtable = Airtable(base_key='appihfkpqStNh6j9v', table_name='Test Cases copy', api_key='keyq6E1toJDkJN4RM')
    tests_case_names = ['test 1', 'test 2']
    # all_records = airtable.get_all()
    # print(all_records)
    # response = False
    # for record in all_records:
    #     if record['fields']['Test Name'] in tests_case_names:
    #         test_id = record['id']
    #         response = airtable.delete(test_id)['deleted']
    #         print(f"Test Name : {record['fields']['Test Name']} \t "
    #               f"Test ID: {test_id}\t"
    #               f"Test Case Deleted Status : {response['deleted']}")
    #         break

    # Delete record by th filed name directly
    for test_case in tests_case_names:
        record = airtable.delete_by_field('Test Name', test_case)
        print(
            f"Test Case Name : {test_case} \t Test Case ID : {record['id']} "
            f"\t Test Case Deletion Status : {record['deleted']}")

    # if response:
    #     print('Record removed')
    # else:
    #     print('Record is not removed')
    pytest.xfail('Script is under development Stage')
