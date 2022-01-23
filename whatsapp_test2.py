import configparser
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

driver = webdriver.Chrome("./chromedriver_win32/chromedriver.exe")
#driver.get("https://web.whatsapp.com")
driver.set_script_timeout(100)

def user_is_logged_in(driver, wait_time):
    '''Checks if the user is logged in to WhatsApp by looking for the pressence of the chat-pane'''

    try:
        chat_pane = WebDriverWait(driver, wait_time).until(
            expected_conditions.presence_of_element_located((By.ID, 'pane-side')))
        return True
    except TimeoutException:
        return False


def whatsapp_is_loaded(driver):
    '''Attempts to load WhatsApp in the browser'''

    print("Loading WhatsApp...", end="\r")

    # Open WhatsApp
    driver.get('https://web.whatsapp.com/')

    # Check if user is already logged in
    logged_in, wait_time = False, 20
    while not logged_in:

        # Try logging in
        logged_in = user_is_logged_in(driver, wait_time)

        # Allow user to try again and extend the wait time for WhatsApp to load
        if not logged_in:
            # Display error to user
            print(
                f"Error: WhatsApp did not load within {wait_time} seconds. Make sure you are logged in and let's try again.")

            is_valid_response = False
            while not is_valid_response:
                # Ask user if they want to try loading WhatsApp again
                err_response = input("Proceed (y/n)? ")

                # Try again
                if err_response.strip().lower() in {'y', 'yes'}:
                    is_valid_response = True
                    continue
                # Abort loading WhatsApp
                elif err_response.strip().lower() in {'n', 'no'}:
                    is_valid_response = True
                    return False
                # Re-prompt the question
                else:
                    is_valid_response = False
                    continue

    # Success
    print("Success! WhatsApp finished loading and is ready.")
    return True


def extract_process():

    # get the name of all the chat contacts
    for chatter in driver.find_elements_by_xpath("//div[@class='_2EXPL']"):
        # now we look for the element with the chat name
        chatter_name = chatter.find_element_by_xpath(".//span[contains(@class, '_1wjpf _3NFp9 _3FXB1')]").text
        print(chatter_name)
        
        # now we get the information in a specific chat
        chatter.find_element_by_xpath(".//div[contains(@class,'_3j7s9')]").click()
        chat_section = driver.find_element_by_xpath(".//div[contains(@class, '_2nmDZ')]")
        
        # scroll until the start of conversation
        while not driver.find_elements_by_xpath(".//span[@data-icon='lock-small']"):
            chat_section.send_keys(Keys.CONTROL + Keys.HOME)
            time.sleep(2)
            
        # create text_file to save messages
        chat_file = open("wa_chats/convo-{}.txt".format(chatter_name), 'w+', encoding="utf8")

        # grab all the messages a
        for messages in driver.find_elements_by_xpath(
            "//div[contains(@class,'message-in')] | //div[contains(@class,'message-out')]"):
            
            final_message = ""
            # get message text and emojis
            try:
                message = ""
                emojis = []

                message_container = messages.find_element_by_xpath(
                    ".//div[@class='copyable-text']")
                
                message_details = message_container.get_attribute("data-pre-plain-text").replace("]", " -").strip("[")
                final_message += message_details
                
                message = message_container.find_element_by_xpath(
                    ".//span[contains(@class,'selectable-text invisible-space copyable-text')]"
                ).text
                final_message += message
                
                for emoji in message_container.find_elements_by_xpath(
                    ".//img[contains(@class,'selectable-text invisible-space copyable-text')]"
                ):
                    emojis.append(emoji.get_attribute("data-plain-text"))
                final_message.join(emojis)
                    
            except NoSuchElementException:  # In case there are only emojis in the message
                try:
                    message = ""
                    emojis = []
                    message_container = messages.find_element_by_xpath(
                        ".//div[@class='copyable-text']")
                    message_details = message_container.get_attribute("data-pre-plain-text").replace("]", " -").strip("[")
                    final_message += message_details
                    for emoji in message_container.find_elements_by_xpath(
                            ".//img[contains(@class,'selectable-text invisible-space copyable-text')]"
                    ):
                        emojis.append(emoji.get_attribute("data-plain-text"))
                    final_message.join(emojis)
                except NoSuchElementException:
                    pass
                
                
            # now, to format the message into a similar style as a whatsapp exported chat
            # format follows the following: dd/mm/yyyy, hh:mm - [username]: [chat_message]
            msg = final_message + "\n"
            chat_file.write(msg)
        chat_file.close()


def main():
    if not whatsapp_is_loaded(driver):
        print("You've quit WhatSoup.")
        driver.quit()
        return

    # Get chats
    #chats = get_chats(driver)
    extract_process()


if __name__ == "__main__":
    main()