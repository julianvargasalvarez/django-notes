def visit(context, path):
    context.selenium.get("%s%s" % (context.live_server_url, path))

def fill_in(context, name, value):
    field = context.find_element_by_name(name)
    field.clear()
    field.send_keys(value)

def submit(context):
    context.find_element_by_css_selector("[type='submit']").click()

def click_on(context, text):
    buttons_or_links = context.find_elements_by_css_selector("[type='submit'],[type='button'],a")
    button_or_link = [element for element in buttons_or_links if text.lower() == (element.get_attribute('value') or element.text).lower()]

    if not len(button_or_link):
        raise IndexError("Button or link with text '%s' not found" % text)

    button_or_link[0].click()

def select_option(context, value, _from):
    select = context.find_element_by_name(_from)
    options = select.find_elements_by_tag_name("option")
    option = [element for element in options if value.lower() == element.text.lower()]

    if not len(option):
        raise IndexError("Option with text '%s' not found" % value)

    option[0].click()

def has_content(context, content):
    return content.lower() in context.text.lower()

def has_link(context, text):
    links = context.find_elements_by_tag_name("a")
    link = [element for element in links if text.lower() == element.text.lower()]
    return len(link) > 0


def login(context, user):
    visit(context, "/accounts/login")

    fill_in(context.selenium, "username", user.get_username())
    fill_in(context.selenium, "password", "12345678")

    submit(context.selenium)
