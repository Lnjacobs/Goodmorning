from Goodmorning import ProductiveMorning

today = ProductiveMorning('Sacramento')

### test checking email
# set up faux email account
today.setUpEmail('socks4fools@gmail.com','xkdjfliiddghyhor')
# check unread emails
today.getEmails()