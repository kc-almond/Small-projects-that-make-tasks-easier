import os
import pandas as pd
import matplotlib.pyplot as plt
from obspy.imaging.beachball import beach

# Load focal mechanism data from CSV
csv_file = "Bohol Sources.csv"  # Replace with your actual CSV filename
df = pd.read_csv(csv_file)

# Create output folder (optional)
output_folder = os.path.dirname(os.path.abspath(__file__))

# Loop through each row and generate beachball diagram
for index, row in df.iterrows():
    event_id = row['ID']
    rup_name = row['Rupture File Name']
    strike = row['Strike']
    dip = row['Dip']
    rake = row['Rake']

    mechanism = [strike, dip, rake]

    # Create figure
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_aspect('equal')
    ax.axis('off')

    # Plot beachball
    bball = beach(mechanism, xy=(0, 0), width=1.8, linewidth=1, facecolor='k', edgecolor='k')
    bball.set_zorder(10)
    ax.add_collection(bball)

    # Title
    ax.set_title(f"{event_id}\nStrike={strike}°, Dip={dip}°, Rake={rake}°", fontsize=10)

    # Save the figure
    output_path = os.path.join(output_folder, f"{event_id}_{rup_name}_beachball.png")
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close(fig)

    print(f"Saved: {output_path}")

print("All beachball diagrams have been generated.")
