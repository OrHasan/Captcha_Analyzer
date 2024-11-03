from matplotlib import pyplot as plt


def comparison_plot(config, img, img_median=None, img_dilation=None, img_erosion=None, multi_step=None):
    if not multi_step:
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

    else:
        fig, axs = plt.subplots(nrows=4, ncols=3)

        axs[0, 0].remove()
        axs[0, 2].remove()
        axs[1, 1].remove()
        axs[2, 1].remove()

        axs[0, 1].imshow(img)
        axs[0, 1].axis('off')
        axs[0, 1].set_title('Captcha')

        axs[1, 0].imshow(multi_step[0])
        axs[1, 0].axis('off')
        axs[1, 0].set_title('Step 1:\nFirst Median Filter\n')

        axs[1, 2].imshow(multi_step[1])
        axs[1, 2].axis('off')
        axs[1, 2].set_title('Step 2:\nFirst Median Filter\n+img as Mask')

        axs[2, 0].imshow(multi_step[2])
        axs[2, 0].axis('off')
        axs[2, 0].set_title('Step 3:\nSecond Median Filter\n')

        axs[2, 2].imshow(multi_step[3])
        axs[2, 2].axis('off')
        axs[2, 2].set_title('Step 4:\nSecond Median Filter\n+img as Mask')

        if len(multi_step) == 5:
            axs[3, 0].remove()
            axs[3, 2].remove()

            axs[3, 1].imshow(multi_step[4])
            axs[3, 1].axis('off')
            axs[3, 1].set_title('Step 5:\n300% Larger Picture\n+Dilation Filter')

        else:
            axs[3, 1].remove()

            axs[3, 0].imshow(multi_step[4])
            axs[3, 0].axis('off')
            axs[3, 0].set_title('Step 5:\n300% Larger Picture\n+Dilation Filter')

            axs[3, 2].imshow(multi_step[5])
            axs[3, 2].axis('off')
            axs[3, 2].set_title('Step 6:\nErosion Filter')

    if config.debug()['show_comparison']:
        plt.show()

    fig.tight_layout()
    return fig
