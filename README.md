<div align="center">

<img src="docs/imgs/sense_core_logo.svg" height="140px">

**State-of-the-art Real-time Action Recognition**

---

<!-- BADGES -->
<p align="center">
    <a href="https://sunnypanchal.ca/">
        <img alt="Documentation" src="https://img.shields.io/website/http/20bn.com.svg?down_color=red&down_message=offline&up_message=online">
    </a>
    <a href="https://github.com/TwentyBN/sense/master/LICENSE">
        <img alt="GitHub" src="https://img.shields.io/github/license/TwentyBN/sense.svg?color=blue">
    </a>
    <a href="https://github.com/TwentyBN/sense/releases">
        <img alt="GitHub release" src="https://img.shields.io/github/release/TwentyBN/sense.svg">
    </a>
    <a href="https://github.com/TwentyBN/sense/blob/master/CODE_OF_CONDUCT.md">
        <img alt="Contributor Covenant" src="https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg">
    </a>
</p>

</div>

---

This is a fork of the [TwentyBn:Sense]() repository where I'll be building a few more demos with Sense. 

For installation instructions and instructions on running the already included demos, check out the readme on the 
main repository. You'll have to also download the pre-trained weights as described there too. 

## RisottoStone

<p align="center">
    <img src="https://raw.githubusercontent.com/sunny-panchal/sense/master/docs/gifs/chopping_garlic.gif" 
width="300px">
    <img src="https://raw.githubusercontent.com/sunny-panchal/sense/master/docs/gifs/keep_stirring_1.gif" width="300px">
</p>

<p align="center">
    <img src="https://raw.githubusercontent.com/sunny-panchal/sense/master/docs/gifs/chilli_to_pot.gif" 
width="300px">
    <img src="https://raw.githubusercontent.com/sunny-panchal/sense/master/docs/gifs/add_rice.gif" width="300px">
</p>

The full video can be found [here](https://drive.google.com/file/d/1GzO_z5SY3D0t3yKOY7mwxREWjGxr9Mbi/view?usp=sharing).

In this fork a "RisottoStone" demo is added which is a cooking assistant that can detect some basic kitchen 
activities. For more details, check out my blogpost on it [here](https://sunnypanchal.ca/projects/risotto-stone).

To run RisottoStone:

```commandline
python examples/run_risotto_stone.py --use_gpu
```

**Note**: This example uses a basic Text-to-speech tool called `spd-say` which is pre-installed in Ubuntu 14.04+. On 
older versions or on MacOS, you'll have to install it manually using `sudo apt install speech-dispatcher`

---

## License 

The code is copyright (c) 2020 Twenty Billion Neurons GmbH under an MIT Licence. See the file LICENSE for details. Note that this license 
only covers the source code of this repo. Pretrained weights come with a separate license available [here](https://20bn.com/licensing/sdk/evaluation).

The code makes use of these sounds from [freesound](https://freesound.org/):
- "[countdown_sound.wav](https://freesound.org/s/244437/)" from "[milton.](https://freesound.org/people/milton./)" licensed under CC0 1.0
- "[done_sound.wav](https://freesound.org/s/388046/)" and "[exit_sound.wav](https://freesound.org/s/388047/)" from "[paep3nguin](https://freesound.org/people/paep3nguin/)" licensed under CC0 1.0
