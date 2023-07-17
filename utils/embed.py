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
        """
        Create a default embed with white color.
        
        Args:
            title (str): The title of the embed.     
            description (str): The description of the embed.  
        
        Returns:          
            disnake.Embed: The default embed.
        """       
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