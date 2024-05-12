'''
    Contains some functions to preprocess the data used in the visualisation.
'''
import pandas as pd
from modes import MODE_TO_COLUMN


def summarize_lines(df):
    '''
        Sums each player's total of number of lines and  its
        corresponding percentage per act.

        The sum of lines per player per act is in a new
        column named 'PlayerLine'.

        The percentage of lines per player per act is
        in a new column named 'PercentCount'

        Args:
            df: The pandas dataframe containing the data from the .csv file
        Returns:
            The modified pandas dataframe containing the
            information described above.
    '''
    # TODO : Modify the dataframe, removing the line content and replacing
    # it by line count and percent per player per act
    df = df.drop(columns=['Scene', 'Line', 'PlayerLine'])
    df['LineCount']=1
    df=df.groupby(by=['Act', 'Player'], axis=0, as_index=False).sum()
    df['PercentCount']=(df.groupby(['Act','Player']).sum(numeric_only=True)['LineCount']/
                            df.groupby('Act').sum(numeric_only=True)['LineCount']).reset_index()['LineCount']*100
    return df


def replace_others(df):
    '''
        For each act, keeps the 5 players with the most lines
        throughout the play and groups the other players
        together in a new line where :

        - The 'Act' column contains the act
        - The 'Player' column contains the value 'OTHER'
        - The 'LineCount' column contains the sum
            of the counts of lines in that act of
            all players who are not in the top
            5 players who have the most lines in
            the play
        - The 'PercentCount' column contains the sum
            of the percentages of lines in that
            act of all the players who are not in the
            top 5 players who have the most lines in
            the play

        Returns:
            The df with all players not in the top
            5 for the play grouped as 'OTHER'
    '''
    # TODO : Replace players in each act not in the top 5 by a
    # new player 'OTHER' which sums their line count and percentage
    
    top_five=df.groupby('Player').LineCount.sum().sort_values(ascending=False).index.values.tolist()[:5]
    acts=[]
    for i in range(1,6):
        act = df.loc[df.Act==i]
        others = act.loc[~act.Player.isin(top_five)][['LineCount','PercentCount']].sum()
        act = pd.concat([act.loc[act.Player.isin(top_five)],pd.DataFrame(data={'Act':i, 'Player':'OTHER', 
                                                        'LineCount':others.LineCount, 'PercentCount':others.PercentCount},index=[0])]
                        ,axis=0, ignore_index=True).sort_values('Player')
        acts.append(act)
    return pd.concat(acts).reset_index().drop(columns='index')


def clean_names(df):
    '''
        In the dataframe, formats the players'
        names so each word start with a capital letter.

        Returns:
            The df with formatted names
    '''
    df['Player']=df.sort_values(['Act','Player']).Player.str.lower().str.title()
    return df
