# coding=utf-8
from handler.darnet.trading_net_handler import DarkNetTradingNet
from handler.breached.breached_handler import BreachedTo
from handler.cabyc.changan_handler import ChangAn


handler_list = {
    'darknet_trading_net': lambda options: DarkNetTradingNet(options),
    'darknet_changan': lambda options: ChangAn(options),
    'breached_breached_io': lambda options: BreachedTo(options),
}