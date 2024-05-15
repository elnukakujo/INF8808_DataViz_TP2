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
        in a new column named 'LinePercent'

        Args:
            df: The pandas dataframe containing the data from the .csv file
        Returns:
            The modified pandas dataframe containing the
            information described above.
    '''
    # TODO : Modify the dataframe, removing the line content and replacing
    
    # We only care about the occurence of characters in each act, we remove useless columns. 
    # Create a new LineCount column and set it as one equally, to then remove the duplicates of characters per act and keep the sum
    df = df.drop(columns=['Scene', 'Line', 'PlayerLine'])
    df['LineCount']=1
    df=df.groupby(by=['Act', 'Player'], axis=0, as_index=False).sum()
    
    # The LinePercent is computed by dividing the LineCount by the sum of the lines in the act, multiplied by 100 to get the percents.
    df['LinePercent']=(df.groupby(['Act','Player']).sum(numeric_only=True)['LineCount']/
                            df.groupby('Act').sum(numeric_only=True)['LineCount']).reset_index()['LineCount']*100
    
    # Rounding here the percents, because I don't know how to round them ONLY in the hypertext
    df['LinePercent']=df.LinePercent.round(2)
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
        - The 'LinePercent' column contains the sum
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
    
    # We find the top five players with the most lines in the total dataframe. To do so, we sum all the players, ignoring the acts, and keep the five biggest. 
    top_five=df.groupby('Player').LineCount.sum().sort_values(ascending=False).index.values.tolist()[:5]
    
    # We iterate in each act to create the others' lines, and add them to the top five
    acts=[]
    for i in range(1,6):
        # We save the df values from the act, sum every player not in the top_five, concatenate the top five players with the new 'others' line 
        act = df.loc[df.Act==i]
        others = act.loc[~act.Player.isin(top_five)][['LineCount','LinePercent']].sum()
        act = pd.concat([act.loc[act.Player.isin(top_five)],pd.DataFrame(data={'Act':i, 'Player':'OTHER', 
                                                        'LineCount':others.LineCount, 'LinePercent':others.LinePercent},index=[0])]
                        ,axis=0, ignore_index=True).sort_values('Player')
        
        # Save the act's dataset in the array containing all the acts done
        acts.append(act)
        
    # We concatenate all the acts together and remove the additional index column
    return pd.concat(acts).reset_index().drop(columns='index')


def clean_names(df):
    '''
        In the dataframe, formats the players'
        names so each word start with a capital letter.

        Returns:
            The df with formatted names
    '''
    # We sort the values in each act like shown in the example, then start by lowering it all (the player names where fully capital until now),
    # then use the title() fct to higher only the first letters
    df['Player']=df.sort_values(['Act','Player']).Player.str.lower().str.title()
    return df
