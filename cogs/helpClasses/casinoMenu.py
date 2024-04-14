import discord.ui


class CasinoMenu(discord.ui.Select):
    def __init__(self):
        options = [
            self.add_option(label="Black Jack", description="Join/Leave Black Jack"),
            self.add_option(label="Roulette", description="Join/Leave Roulette")
        ]
        placeholder = "Choose with which game you want to interact"

        super().__init__(options=options, placeholder=placeholder)