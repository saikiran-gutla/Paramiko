import pytest
import ssl
import jenkins


@pytest.mark.xfail(run=False)
def test_jenkins():
    ssl._create_default_https_context = ssl._create_unverified_context
    # def test_getSCMInfroFromLatestGoodBuild(url, jobName, username=None, password=None):
    #     J = Jenkins(url, username, password)
    #     job = J[jobName]
    #     lgb = job.get_last_good_build()
    #     return lgb.get_revision()
    #
    #
    # if __name__ == '__main__':
    #     print(test_getSCMInfroFromLatestGoodBuild(url='https://build.automox-dev.com:4443', jobName='axtest',
    #                                               username='saikiran_gutla', password='Qzixb6asai'))

    server = jenkins.Jenkins('https://build.automox-dev.com:4443/job/', username='saikiran_gutla',
                             password='Qzixb6asai', timeout=60)
    print(server)
    job_info = server.get_job_info('test-advanced-policy', depth=0, fetch_all_builds=False)
    print(job_info)
    # jobs = server.get_all_jobs(folder_depth=None)
    # print(f'Jobs : {jobs}')
    # for job in jobs:
    #     print(job['fullname'])
    pytest.xfail('Script is not completed')
