from user_agents import parse

ua_list = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201",
    "user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"

]
for ua in ua_list:
    print(str(parse(ua)))

# sys_opt = str(parse(ua)).split("/")
# print(sys_opt[1].strip())


# # iPhone的UA例子
# ua_string = 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/7534.48.3'
# user_agent = parse(ua_string)
#
# # 浏览器属性
# user_agent.browser  # returns Browser(family=u'Mobile Safari', version=(5, 1), version_string='5.1')
# user_agent.browser.family  # returns 'Mobile Safari'
# user_agent.browser.version  # returns (5, 1)
# user_agent.browser.version_string  # returns '5.1'
#
# # 操作系统属性
# user_agent.os  # returns OperatingSystem(family=u'iOS', version=(5, 1), version_string='5.1')
# user_agent.os.family  # returns 'iOS'
# user_agent.os.version  # returns (5, 1)
# user_agent.os.version_string  # returns '5.1'
#
# # 设备属性
# user_agent.device  # returns Device(family=u'iPhone', brand=u'Apple', model=u'iPhone')
# user_agent.device.family  # returns 'iPhone'
# user_agent.device.brand  # returns 'Apple'
# user_agent.device.model  # returns 'iPhone'
#
# # 字符串版本
# print(str(user_agent))  # returns "iPhone / iOS 5.1 / Mobile Safari 5.1"
