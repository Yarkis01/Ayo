import disnake

class Embed:
    """A class for creating different embed types."""
    
    @staticmethod    
    def make_embed(color, title, description):
        """Create an embed with the given color and info.
        
        Args: 
            color (int): Embed color in hexadecimal.
            title (str): Embed title.
            description (str): Embed description.
        
        Returns:
            disnake.Embed: The created embed.
        """
        return disnake.Embed(
            title=title,
            description=description,     
            color=color
        ).set_footer(
            text = "Réalisé avec ❤️ par Yarkis01",     
            icon_url = "https://avatars.githubusercontent.com/u/109750019?v=4"  
        )
            
    @staticmethod       
    def default(title: str, description: str) -> disnake.Embed:      
        """Create a default embed with white color."""       
        return Embed.make_embed(0xffffff, title, description)
        
    @staticmethod       
    def error(title: str, description: str) -> disnake.Embed:
        """Create an error embed with red color."""
        return Embed.make_embed(0xe74c3c, title, description)
        
    @staticmethod       
    def success(title: str, description: str) -> disnake.Embed:   
        """Create a success embed with green color."""    
        return Embed.make_embed(0x2ecc71, title, description)
    
    @staticmethod       
    def warning(title: str, description: str) -> disnake.Embed:   
        """Create a warning embed with yellow color."""   
        return Embed.make_embed(0xf1c40f, title, description)
    
    @staticmethod
    def splatoon2(title: str, description: str, color: int = 0xf03c78) -> disnake.Embed:
        """Create a Splatoon 2 embed"""
        return Embed.make_embed(color, f"<:Splatoon2:1036691271076560936> {title}", description).set_footer(text = "Données provenant de l'API du site Splatoon2.ink", icon_url = "https://i.imgur.com/nvxf5TK.png")
    
    @staticmethod
    def splatoon3(title: str, description: str, color: int = 0xebeb3f) -> disnake.Embed:
        """Create a Splatoon 3 embed"""
        return Embed.make_embed(color, f"<:Splatoon3:1036691272871718963> {title}", description).set_footer(text = "Données provenant de l'API du site Splatoon3.ink", icon_url = "https://i.imgur.com/Ufv6yH4.png")