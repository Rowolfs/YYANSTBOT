from commandflow.commands.base import StepCommand
from commandflow.core import QueueCommands



@QueueCommands.register
class PrintHello(StepCommand):
    name = "print_hello"

    async def run(self, message, state, **context):
        await message.answer("Hello, World!")
        await self.next()



