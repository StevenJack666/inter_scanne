

from tg_spiders.cli.telegram_clear_dialog import TelegramClearDialog
from tg_spiders.cli.telegram_connect_final import *
from tg_spiders.cli.telegram_get_dialog import *
from tg_spiders.cli.telegram_get_message import *
from tg_spiders.cli.telegram_get_user_photo import *
from tg_spiders.cli.telegram_group_final import *
from tg_spiders.cli.telegram_group_member_final import *
from tg_spiders.cli.telegram_send_msg_final import *

tg_handler_list = {
    'clear_dialog': lambda options, app_conf: TelegramClearDialog(options, app_conf),
    'connect': lambda options, app_conf: TelegramConnectFinal(options, app_conf),
    'get_dialog': lambda options, app_conf: TelegramGetDialog(options, app_conf),

    'get_message': lambda options, app_conf: TelegramGetMessage(options, app_conf),
    'user_photo': lambda options, app_conf: TelegramGetUserPhoto(options, app_conf),
    'group_final': lambda options, app_conf: TelegramGroupFinal(options, app_conf),

    'member_final': lambda options, app_conf: TelegramGroupMemberFinal(options, app_conf),
    'send_msg': lambda options, app_conf: TelegramSenfMsgFinal(options, app_conf),
}