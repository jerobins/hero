"""
   HERO - Home Energy Report Online(?)

   https://github.com/jerobins/hero

"""
import requests, sys, datetime, json, random, logging

class hero:

   def _getCredentials(self, username, password):
      """ End-point discovery and Oauth token request.
      Params:
         username - for HER dashboard
         password - for HER dashboard

      Returns: hero object
      """

      # i'm guessing this numeric param is just to ensure no cacheing of the end-point info
      # for giggles made it a random int, probably not needed at all
      params = { "x": random.randint(10000, 999999) }
      endpoint = self.her_host

      try:
         r = requests.get(endpoint, params=params)
      except Exception as e:
         logging.critical(e)
         sys.exit(e)

      if r.status_code != 200:
         logging.critical(r)
         sys.exit(r)

      result = r.json()

      if 'fault' in result:
         logging.critical(result)
         sys.exit(result)

      logging.debug(result)

      self.hero_api = result["heroApi"]
      form_data = { "grant_type": "password", 
                    "username": username, 
                    "password": password }

      try:
         r = requests.post(result["authApi"], 
                           data=form_data, 
                           auth=(result["consumerKey"], 
                           result["consumerSecret"]))
      except Exception as e:
         logging.critical(e)
         sys.exit(e)

      if r.status_code != 200:
         logging.critical(r)
         sys.exit(r)

      result = r.json()

      if 'errorResponse' in result:
         logging.critical(result)
         sys.exit(result)

      logging.debug(result)

      # token lifetime is 30 mins.
      self.hero_api_token = result["access_token"]

      params = { "loginIdentity": result["email"], 
                 "cdpId": result["cdp_internal_user_id"] }

      endpoint = self.hero_api + self.api_account
      headers = { "Authorization": "Bearer " + self.hero_api_token }

      try:
         r = requests.get(endpoint, params=params, headers=headers)
      except Exception as e:
         logging.critical(e)
         sys.exit(e)

      if r.status_code != 200:
         logging.critical(r)
         sys.exit(r)

      result = r.json()

      logging.debug(result)

      if 'errorResponse' in result:
         logging.critical(result)
         sys.exit(result)

      self.hero_account_id = result[0]["hubAcctId"]

      return

   def getDailyUsage(self, timestamp):
      """
      """

      endpoint = self.hero_api + self.api_dailydata
      params= { "accountId": self.hero_account_id, 
                "intervalDate": timestamp.strftime("%Y-%m-%d") }
      headers = { "Authorization": "Bearer " + self.hero_api_token }

      try:
         r = requests.get(endpoint, params=params, headers=headers)
      except Exception as e:
         logging.critical(e)
         sys.exit(e)

      if r.status_code != 200:
         logging.critical(r)
         result = {}
      else:
         result = r.json()
         logging.debug(result)
         result = result["usagesFifteen"]

      return result

   def getCurrentUsageDetail(self, billCycleEndDate):
      """
      """

      endpoint = self.hero_api + self.api_usage
      params= { "accountId": self.hero_account_id,
                "billCycleEndDate": billCycleEndDate.strftime("%Y-%m-%d") }
      headers = { "Authorization": "Bearer " + self.hero_api_token }

      try:
         r = requests.get(endpoint, params=params, headers=headers)
      except Exception as e:
         logging.critical(e)
         sys.exit(e)

      if r.status_code != 200:
         logging.critical(r)
         result = {}
      else:
         result = r.json()
         logging.debug(result)

      return result

   def __init__(self, username, password):
      self.hero_api = ""
      self.hero_api_token = ""
      self.hero_account_id = ""

      self.her_host = "https://her.duke-energy.com/config/config.prod.json"
      self.api_account = "/user/accounts"
      self.api_dailydata = "/usage/comparison/daily/one-day"
      self.api_usage = "/usage/detail"
      self.api_billing_cycle = "/usage/latest-billing-cycle"
      # to test
      self.api_energy_profile = "/home-energy-profile" # hubAccountId
      self.api_two_year_billing_cycle = "/usage/two-years-billing-cycle" # hubAccountId
      self.api_card = "/card" # hubAccountId
      self.api_cohort = "/cohort" # hubAccountId
      self.api_account_id = "/user/account-id" # accountNumber
      self.api_monthlydata = "/usage/comparison/daily/one-month" # hubAccountId, startDate, endDate, heroUsageCategoryEnum?
      self.api_load = "/load/disaggregation" # hubAccountId, billCycleEndDate

      self._getCredentials(username, password)
      return
