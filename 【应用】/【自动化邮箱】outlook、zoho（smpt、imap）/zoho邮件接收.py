# 把所有发到自己域名的邮件全部转发到outlook邮箱。从outlook里读就好了
# 目前都是cf解析出来的邮箱，就是怎么设置的问题
import datetime
# pip install imbox
from imbox import Imbox
# outlook_F141E181C147041E@outlook.com#邮箱名称
with Imbox('imap-mail.outlook.com',
        username='1348006516@qq.com',#账号
        password='wth000',#密码
        ssl=True,
        ssl_context=None,
        starttls=False) as imbox:

    # Get all folders
    status, folders_with_additional_info = imbox.folders()

    # Gets all messages from the inbox
    all_inbox_messages = imbox.messages()

    # # Unread messages
    # unread_inbox_messages = imbox.messages(unread=True)

    # # Flagged messages
    # inbox_flagged_messages = imbox.messages(flagged=True)

    # # Un-flagged messages
    # inbox_unflagged_messages = imbox.messages(unflagged=True)

    # # Flagged messages
    # flagged_messages = imbox.messages(flagged=True)

    # # Un-flagged messages
    # unflagged_messages = imbox.messages(unflagged=True)

    # # Messages sent FROM
    # inbox_messages_from = imbox.messages(sent_from='sender@example.org')

    # # Messages sent TO
    # inbox_messages_to = imbox.messages(sent_to='receiver@example.org')

    # # Messages received before specific date
    # inbox_messages_received_before = imbox.messages(date__lt=datetime.date(2018, 7, 31))

    # # Messages received after specific date
    # inbox_messages_received_after = imbox.messages(date__gt=datetime.date(2018, 7, 30))

    # # Messages received on a specific date
    # inbox_messages_received_on_date = imbox.messages(date__on=datetime.date(2018, 7, 30))

    # # Messages whose subjects contain a string
    # inbox_messages_subject_christmas = imbox.messages(subject='Christmas')

    # # Messages whose UID is greater than 1050
    # inbox_messages_uids_greater_than_1050 = imbox.messages(uid__range='1050:*')

    # # Messages from a specific folder
    # messages_in_folder_social = imbox.messages(folder='Social')

    # # Some of Gmail's IMAP Extensions are supported (label and raw):
    # all_messages_with_an_attachment_from_martin = imbox.messages(folder='all', raw='from:martin@amon.cx has:attachment')
    # all_messages_labeled_finance = imbox.messages(folder='all', label='finance')

    for uid, message in all_inbox_messages:
    # Every message is an object with the following keys

        print(message.sent_from)
        print(message.sent_to)
        print(message.subject)
        print(message.headers)
        print(message.message_id)
        print(message.date)
        print(message.body["plain"])
        input("next?")