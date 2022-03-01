import pandas as pd
import os

from pandas.core import indexing

sorted_files = sorted(os.listdir("data"))
for i in sorted_files:
    print(i)

#notes: 
#1. make sure to filter out "daily" csv files
#2. Make use of "0000_merge_timestamp" as name to ensure
# that merged files always get priority across different
# coin folders
#3. In the future, when these files become larger, the current merging
#techique may become slow and will need better testing of the match finding
#technique used to find the merge location. I believe it is O(n) but the average can be
#easily reduced by implementing something like binary search tree

merged_df = pd.DataFrame()

for i in range(len(sorted_files)):
    if ("lock" not in str(i)):
        print(i)
        
        file_loc = "data/"+ str(sorted_files[i])
        tmp_df = pd.read_csv(file_loc)

        #TODO: Below, unix_timestamp column is used a number of times.
        # some of the older data files do not have that column,
        # and may need to have it generated from the datetime where it does not exist
        if (not merged_df.empty):
            match_df = merged_df[merged_df['unix_timestamp']==tmp_df['unix_timestamp'][0]]
            #print(match_df)
            if (not match_df.empty):
                match_index = merged_df[merged_df['unix_timestamp']==tmp_df['unix_timestamp'][0]].index[0]
                print(match_index)
                merged_df = pd.concat([merged_df.head(match_index), tmp_df], sort=False, ignore_index=True)
            else:
                print("No matching index, merging entire dataframes")
                merged_df = pd.concat([merged_df, tmp_df], sort=False, ignore_index=True)
            #row_count = tmp_df.shape[0]  #Getting the length of the index instead might be microseconds quicker,
            #print(row_count)             #but this should protect more against inconsistent indexing if my structure changes

            #print(merged_df)

        else:
            merged_df = tmp_df

        #print("----------------")

merged_df.to_csv("0000_merge_test.csv")