from playwright.async_api import async_playwright
import asyncio
import sys
import pandas as pd
import re
from datetime import datetime

# Variable merge from ui.R.
username = "Josh9182"
password = "PythonPython642"
jfdt = "C:\\Users\\josh9182\\Documents\\Important Files\\customer_contacts.json"

async def login(username, password, jfdt): # Asynchronous Playwright function requiring application username, password, and json file.
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False) 
        page = await browser.new_page() # "browser" & "page" variables automatically initiating chrome window and new tab once function is launched.

        await page.goto("https://website.org/COOLPLACE")
        await page.click('input[name="userIDfield"]')
        await page.fill('input[name="userIDfield"]', username)
        await page.click('input[name="passwordIDfield"]')
        await page.fill('input[name="passwordIDfield"]', password)
        await page.click('button[name="SignInButton"]')
        await page.click('button[name="IAgreeButton"]') # Accessing template website and inputting username & password while getting past an "I Agree" notification.
        
        fdt = pd.read_json(jfdt) # Reading JSON DataFrame featuring customer information.
        fdt = fdt.applymap(lambda x: str(int(x)) if pd.notnull(x) and type(x) == float or type(x) == int else x) # Lambda function being applied to every cell in the "fdt" DataFrame, eliminating possible decimals and ensuring all data is formatted as a str for easier use via Python.  

        def eotd(value): # eotd function, "Eleven or Twelve Digits". Ensuring no incorrect customer ID information is sent into the organization software. 
            return bool(re.match(r'^\d{11}$|^\d{12}$', value))

        filtered_dt = fdt.applymap(eotd) # New DataTable with each cell affected by the "eotd" function.
        filtered_values = fdt[filtered_dt].stack().tolist() # Applying the new DataFrame to our original and converting into list, allowing for fluid selection.

        time = datetime.now() 
        fd = time.strftime("%m/%d") # Value for current month and day of automation, necessary for customer information change logging. 

        for value in filtered_values:
            await page.click('button[data-qa="CustomerInformationChange"]')
            await page.click('input[data-qa="CIC.gridView3.group1.CICSearch1"]')
            await page.fill('input[data-qa="CIC.gridView3.group1.CICSearch1"]', f"*{value}")
            await page.click('button[data-qa="CIC.gridView3.group1.CICSearch1.searchActions.search"]') # For loop navigating through "Customer Information Change" and inputting customer information for each individual. 

            await page.click('td[data-qa="CIC.gridView3.group1.grid1.rows.1.three_dot_menu_CIC"]')
            await page.click('button[data-qa="CIC.gridView3.group1.grid1.rows.1.three_dot_menu_CIC.row1.rowMenu.CIC_DIALOG_ZZ54RT5"]')
            await page.click('button[data-qa="CIC.gridView3.group1.grid1.rows.1.three_dot_menu_CIC_Finalize_ChangeMenu_7Y6t&*%H&%]') # Clicking through 3 dot menu, navigating to the "Finalize Change Menu". 

            input_reason = page.locator('select[data-qa="CIC.gridView3.group1.grid1.rows.1.three_dot_menu_CIC.CIC_DIALOG_InputReason_ZZ54RT5"]') 
            reason_input = await input_reason.input_value() # Locating "Input Reason" input value.

            if reason_input != "": # If reason_input is not empty, it changes value to be empty, also known as the placeholder element "|| Reason ||".
                await input_reason.select_option(value="")
            else:
                print("Proceeding to automation...") 

            await page.click('input[data-qa="CIC.gridView3.group1.CIC.sassScalar1.FCIS"]')
            await page.fill('input[data-qa="CIC.gridView3.group1.CIC.sassScalar1.FCIS"]', f"{fd} LOGGED")
            await page.click('button[data-qa="CIC.gridView3.group1.CIC.sassScalar1.FCIS.CIC_Actions.saveClose"]')
            await page.click('button[data-qa="CIC.profile.Home"]') # Logs "fd" date value combined with "LOGGED", goes back to home screen and restarts the loop.


asyncio.run(login(username, password, jfdt))
