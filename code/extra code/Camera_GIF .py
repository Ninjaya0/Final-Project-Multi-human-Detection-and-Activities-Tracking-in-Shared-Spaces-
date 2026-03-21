#!/usr/bin/env python
# coding: utf-8

# In[4]:


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

BASE = r"C:\Users\DellG5\Desktop\TENNIS DATA"

FOLDERS = {
    "Forehand": os.path.join(BASE, "forehand_v2_resampled"),
    "Backhand": os.path.join(BASE, "backhand_v3_resampled"),
    "Serve":    os.path.join(BASE, "serve_v3_resampled"),
}


CONNECTIONS = [
    (0, 1),   
    (1, 2),   
    (2, 6),  
    (3, 4),   
    (4, 5),   
    (5, 7),   
    (2, 5),   
    (6, 7),   
    (6, 8),  
    (7, 9),   
    (2, 10),  
    (5, 10),  
]

COLORS = {
    "Forehand": "#00C850",
    "Backhand": "#C85000",
    "Serve":    "#0050FF"
}

def load_clips(folder):
    clips = []
    for f in sorted(os.listdir(folder)):
        if f.endswith(".npy"):
            data = np.load(os.path.join(folder, f)) 
            clips.append(data)
    return np.array(clips)  

def compute_mean_clip(clips):
    return clips.mean(axis=0) 

for stroke_name, folder in FOLDERS.items():
    print(f"Processing {stroke_name}...", end=" ")

    clips = load_clips(folder)
    mean_clip = compute_mean_clip(clips)  

    color = COLORS[stroke_name]

    fig, ax = plt.subplots(figsize=(5, 8))
    ax.set_xlim(-0.5, 0.5)
    ax.set_ylim(-0.6, 0.6)
    ax.set_facecolor("#111111")
    fig.patch.set_facecolor("#111111")
    ax.invert_yaxis()  
    ax.set_title(f"Mean {stroke_name} Motion", color="white", fontsize=14, pad=10)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    joint_scatter = ax.scatter([], [], s=80, c=color, zorder=5)
    lines = [ax.plot([], [], color=color, lw=2.5, alpha=0.85)[0] for _ in CONNECTIONS]
    frame_label = ax.text(0, 0.55, '', color='white', ha='center', fontsize=11)

    def init():
        joint_scatter.set_offsets(np.empty((0, 2)))
        for ln in lines:
            ln.set_data([], [])
        frame_label.set_text('')
        return [joint_scatter, frame_label] + lines

    def update(frame_idx, mean_clip=mean_clip):
        pts = mean_clip[frame_idx]  
        xs = pts[:, 0]
        ys = pts[:, 1]
        joint_scatter.set_offsets(np.column_stack([xs, ys]))
        for k, (a, b) in enumerate(CONNECTIONS):
            lines[k].set_data([xs[a], xs[b]], [ys[a], ys[b]])
        frame_label.set_text(f"Frame {frame_idx + 1} / 30")
        return [joint_scatter, frame_label] + lines

    ani = animation.FuncAnimation(
        fig, update, frames=30, init_func=init,
        interval=80, blit=True
    )

  
    out_path = os.path.join(BASE, f"{stroke_name.lower()}_animation.gif")
    ani.save(out_path, writer='pillow', fps=12,
             savefig_kwargs={'facecolor': '#111111'})
    plt.close()
    print(f" Saved → {out_path}")

print("\n All 3 animations saved to TENNIS DATA folder!")
print("Files: forehand_animation.gif, backhand_animation.gif, serve_animation.gif")


# In[ ]:




