import schedule
import time
import subprocess

def run_all_job():
    subprocess.call(["python3", "scraper.py"], cwd="newsscraper/")

schedule.every().day.at("10:00").until("11:30").do(run_all_job)
schedule.every().day.at("22:00").until("23:30").do(run_all_job)

while True:
    schedule.run_pending()
    time.sleep(1)