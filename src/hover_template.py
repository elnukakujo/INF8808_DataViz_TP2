'''
    Provides the template for the hover tooltips.
'''
from modes import MODES


def get_hover_template(name, mode):
    '''
        Sets the template for the hover tooltips.

        The template contains:
            * A title stating player name with:
                - Font family: Grenze Gotisch
                - Font size: 24px
                - Font color: Black
            * The number of lines spoken by the player, formatted as:
                - The number of lines if the mode is 'Count ("X lines").
                - The percent of lines fomatted with two
                    decimal points followed by a '%' symbol
                    if the mode is 'Percent' ("Y% of lines").

        Args:
            name: The hovered element's player's name
            mode: The current display mode
        Returns:
            The hover template with the elements descibed above
    '''
    # TODO: Generate and return the over template
    if mode=='LineCount':
        return '<span style="font-family: Grenze Gotisch; font-size: 24px; font-color: Black">%{x}</span><br></br>'+f'<b>Player:</b> {name}'+'<br><b>Lines: </b>%{y}</br><extra></extra>'
    else:
        return '<span style="font-family: Grenze Gotisch; font-size: 24px; font-color: Black">%{x}</span><br></br>'+f'<b>Player:</b> {name}'+'<br><b>Lines: </b>%{y}</br><extra></extra>'
    
    
    """custom=[['<BR><b>Preço: </b> R$ '+str(name.loc[i, name])]
              for i in name.index]
    
    if mode =='count':
        return ('%{custom}<br><b>Player</b>: %{x}</br><br><b>Lines</b>: %{y}</br>')
    else:
        return ('%{name}'+'<br><b>Player</b>: %{x}</br>'+'<br><b>Percent</b>: %{y:.2f}%</br>')"""
