'''
    Contains some functions related to the creation of the bar chart.
    The bar chart displays the data either as counts or as percentages.
'''

import plotly.graph_objects as go
import plotly.io as pio

from hover_template import get_hover_template
from modes import MODES, MODE_TO_COLUMN


def init_figure():
    '''
        Initializes the Graph Object figure used to display the bar chart.
        Sets the template to be used to "simple_white" as a base with
        our custom template on top. Sets the title to 'Lines per act'

        Returns:
            fig: The figure which will display the bar chart
    '''
    fig = go.Figure()
    
    # TODO : Update the template to include our new theme and set the title
    fig.update_layout(
        template=pio.templates["simple_white+mytemplate"], #To use our template with the simple_white template
        dragmode=False,
        barmode='relative',
        title='Lines per act',
        xaxis = dict(
            tickmode = 'array',
            tickvals = [1,2,3,4,5],
            ticktext = ['Act '+str(i) for i in range(1,6)]
        ) # To add the acts under each category on the xaxis
    )
    return fig


def draw(fig, data, mode):
    '''
        Draws the bar chart.

        Arg:
            fig: The figure comprising the bar chart
            data: The data to be displayed
            mode: Whether to display the count or percent data.
        Returns:
            fig: The figure comprising the drawn bar chart
    '''
    fig = go.Figure(fig)  # conversion back to Graph Object
    # TODO : Update the figure's data according to the selected mode
    
    # We remove all previous data on the figure
    fig.data=[]
    lineMode = MODE_TO_COLUMN[f'{mode}']
    # Create the list of all characters in the data
    playerList = data.Player.unique()
    
    # Not Working :/
    for player in playerList:
        fig.add_trace(go.Bar(
            name=player,
            x=data.loc[data.Player==player].Act,
            y=data.loc[data.Player==player][f'{lineMode}'],
            hovertemplate=get_hover_template(player, lineMode)
        ))
    
    # Update the y-axis legend
    return update_y_axis(fig, mode) 


def update_y_axis(fig, mode):
    '''
        Updates the y axis to say 'Lines (%)' or 'Lines (Count) depending on
        the current display.

        Args:
            mode: Current display mode
        Returns: 
            The updated figure
    '''
    # TODO : Update the y axis title according to the current mode
    if mode=='Percent':
        fig.update_layout(
            yaxis_title='Lines (%)'
        )
    else:
        fig.update_layout(
            yaxis_title=f'Lines({mode})'
        )
    return fig