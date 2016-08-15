#! /usr/bin/python3

from googleads import adwords
import suds
import datetime
import sys

def main(campaignService, adgroupService, reportDownloader):
    try:
        getAndSaveKeywordReport(reportDownloader, getAdGroupIds(adgroupService, getCampaignIds(campaignService)))
        print('Done!')
    except suds.WebFault as e:
        print(e)

def getCampaignIds(service):
    return service.get({
        'fields': ['Id']
    })['entries']

def getAdGroupIds(service, campaignIds):
    selector = {
        'fields': ['Id'],
        'predicates': [
            {
                'field': 'CampaignId',
                'operator': 'EQUALS',
                'values': []
            }
        ]
    }
    ids = []
    for campaignId in campaignIds:
        selector['predicates'][0]['values'] = [campaignId['id']]
        response = service.get(selector)
        for entry in response['entries']:
            ids.append(entry['id'])

    return ids

def getAndSaveKeywordReport(downloader, adgroupIds):
    with open('./test.csv', 'w') as reportFile:
        print('Writing to file')
        reportFile.write(
            downloader.DownloadReportAsString(
                {
                    'reportName': 'Keyword Performance Report - UTC ' + datetime.datetime.now().strftime('%y-%m-%d'),
                    'downloadFormat': 'CSV',
                    'dateRangeType': 'LAST_30_DAYS',
                    'reportType': 'KEYWORDS_PERFORMANCE_REPORT',
                    'selector': {
                        'fields': ['Status', 'Criteria', 'HasQualityScore', 'QualityScore', 'SearchPredictedCtr', 'CreativeQualityScore', 'PostClickQualityScore', 'Impressions', 'Clicks', 'AdGroupId', 'AdGroupName', 'CampaignId', 'CampaignName', 'KeywordMatchType']
                    }
                },
                skip_report_header=False, skip_column_header=False
            )
        )


def createCampaignService(client):
    return client.GetService('CampaignService', version='v201607')

def createAdGroupService(client):
    return client.GetService('AdGroupService', version='v201607')

def createReportDownloader(client):
    return client.GetReportDownloader(version='v201607')

if __name__ == '__main__':
    adwords_client = adwords.AdWordsClient.LoadFromStorage()
    campaignService = createCampaignService(adwords_client)
    adgroupService = createAdGroupService(adwords_client)
    reportDownloader = createReportDownloader(adwords_client)

    main(campaignService, adgroupService, reportDownloader)
