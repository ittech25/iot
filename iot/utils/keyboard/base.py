import logging

from telegram import (
    InlineKeyboardButton, InlineKeyboardMarkup
)


logger = logging.getLogger(__name__)


CLOSE_INLINE_KEYBOARD_COMMAND = "close_keyboard"


class InlineKeyboardMixin:

    def build_keyboard(self, buttons, cols, header_buttons=None, footer_buttons=None):
        if cols > 0:
            kb = [buttons[i:i + cols] for i in range(0, len(buttons), cols)]
        else:
            kb = [[b] for b in buttons]

        if header_buttons:
            kb.insert(0, header_buttons)
        if footer_buttons:
            kb.append(footer_buttons)

        return kb

    def build_inline_keyboard_markup(self, keyboard):
        return InlineKeyboardMarkup(keyboard)

    def header_buttons(self, *args, **kwargs):
        """Returns list of header buttons"""
        pass

    def footer_buttons(self, *args, **kwargs):
        """Returns list of footer buttons"""
        pass

    def back_button(self, *args, **kwargs):
        """
        Returns InlineKeyboardButton with
        callback_data for previous menu
        """
        pass

    def close_button(self):
        return InlineKeyboardButton(
            "Close",
            callback_data=self.return_cb_data(CLOSE_INLINE_KEYBOARD_COMMAND)
        )

    def construct_keyboard_markup(self, *args, **kwargs):
        raise NotImplementedError

    def handle_close(self, text, query, bot, update):
        bot.edit_message_text(text=text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=None)

        self.answer_query(query, bot)


class KeyboardCallBackQueryHandler:

    __slots__ = ("server", "handler_name")

    def __init__(self, server, handler_name):
        self.server = server
        self.handler_name = handler_name

    def return_cb_data(self, cb_data):
        """Always add handler_name before cb_data"""
        return "{} {}".format(self.handler_name, cb_data)

    def answer_query(self, query, bot, text=None, alert=False):
        bot.answer_callback_query(query.id, text=text, show_alert=alert)

    def process_query(self, bot, update, internal_callback_data):
        query = update.callback_query
        logger.info(
            "CMD %s CB Handler: Handling '%s', Internal: %s",
            self.handler_name, query.data, internal_callback_data
        )

        # query_data is only the device's id
        query_data = internal_callback_data.split()

        return query, query_data