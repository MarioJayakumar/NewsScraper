import schedule
import time
import subprocess

def run_all_job():
    subprocess.call(["python3", "scraper.py"], cwd="newsscraper/")

schedule.every().day.at("10:00").do(run_all_job)
#schedule.every().day.at("22:00").do(run_all_job)

schedule.run_all()