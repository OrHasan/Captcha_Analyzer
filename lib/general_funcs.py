import re
from os import listdir
from os.path import isfile, join
from matplotlib import pyplot as plt


def get_file_index(history_dir):
    history_files = [f for f in listdir(history_dir) if isfile(join(history_dir, f))]
    current_index = 0
    for file_name in history_files:
        current_index = max(current_index, int(re.search(r'#(\d+)', file_name).group(1)))
    current_index += 1

    return current_index


def comparison_plot(config, img, img_median, img_dilation, img_erosion):
    if img_median is None:
        fig, axs = plt.subplots(nrows=2, ncols=3)

        axs[0, 0].remove()
        axs[0, 2].remove()
        axs[1, 1].remove()

        axs[0, 1].imshow(img)
        axs[0, 1].axis('off')
        axs[0, 1].set_title('Captcha')

        axs[1, 0].imshow(img_dilation)
        axs[1, 0].axis('off')
        axs[1, 0].set_title('Step 1:\nDilation Filter')

        axs[1, 2].imshow(img_erosion)
        axs[1, 2].axis('off')
        axs[1, 2].set_title('Step 2:\nErosion Filter')

    elif img_dilation is None:
        fig, axs = plt.subplots(nrows=2, ncols=1)

        axs[0].imshow(img)
        axs[0].axis('off')
        axs[0].set_title('Captcha')

        axs[1].imshow(img_median)
        axs[1].axis('off')
        axs[1].set_title('Step 1:\nMedian Filter')

    else:
        fig, axs = plt.subplots(nrows=2, ncols=3)

        axs[0, 0].remove()
        axs[0, 2].remove()

        axs[0, 1].imshow(img)
        axs[0, 1].axis('off')
        axs[0, 1].set_title('Captcha')

        axs[1, 0].imshow(img_median)
        axs[1, 0].axis('off')
        axs[1, 0].set_title('Step 1:\nMedian Filter')

        axs[1, 1].imshow(img_dilation)
        axs[1, 1].axis('off')
        axs[1, 1].set_title('Step 2:\nDilation Filter')

        axs[1, 2].imshow(img_erosion)
        axs[1, 2].axis('off')
        axs[1, 2].set_title('Step 3:\nErosion Filter')

    if config.debug()['show_comparison']:
        plt.show()

    return fig
