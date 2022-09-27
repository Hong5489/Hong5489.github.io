---
layout: post
title: Gate Protocol
subtitle: Breaking Gate Protocol with Flipper Zero
tags: [flipperzero,protocol,frequency]
comments: true
---

Do you know that we can technically brute force our house gate if using static code?

Got my hacker toy *Flipper Zero* last 2 weeks, and I was playing with my cards, TV remotes, gate remote etc. It was FUN!😊

I saw someone implement a Sub-GHz bruteforce plugin in [Unleased Firmware](https://github.com/Eng1n33r/flipperzero-firmware)

So I wonder is my house gate bruteforcable? 

Then after some researching I found [this article by Andre Ng](https://medium.com/csg-govtech/breaking-protocol-d3988fa85eef)

This article explains how he analyse the gate remote protocol and attempt the brute force, which inspire me to investigate my house gate remote, and how to implement the brute force attack on flipper

If you have an Arduino maybe can test his code out

# Tear Down

![unilarm](/uploads/gate/unilarm.JPG){: width="500" }

I up open my gate remote, although its UNILARM brand and not using SMC5326 chip but saw the same DIP switch as describe in the medium article!

Thats means both remote should be using similar protocol!

# Analyse Remote Signal

Then I analyse my remote signal using my flipperzero, save the raw signal and open it on [Pulse Plotter](https://my.flipp.dev/pulse-plotter) to see the signal in pulse

As you can see, my remote signal also using the same encoding, a thin pulse follow by a big gap is `0`, a thick pulse follow by a small gap is `1`:

![pulse](/uploads/gate/pulse.png)

For example:

![pulse2](/uploads/gate/pulse2.png)


First, I compare the signal of button 1 and button 2 (For my remote, button 1 is only open one side of gate, button 2 is open both sides)

According to the article I read, the 17th to 25th bits should be the instruction base (last bit is Synchronisation bit), so instruction base for button 1 is `110000000` and button 2 is `001100000`

Button 1:

![gate1](/uploads/gate/gate1.png)

Button 2:

![gate2](/uploads/gate/gate2.png)

# DIP switch

We have 8 switches and we can switch up, center and down. Means only 3^8 combination! 

I analysed the signal for different combination of DIP switch, it is using the same "encoding" as the SMC5326 remote!

We can refer the figure below to calculate the encoding of the remote:

![dip](/uploads/gate/dip.png)

For example, if the DIP switch is toggled like picture below:

![dip2](/uploads/gate/dip2.png)

```
Follow the figure we get:
24+21+22+19+20+18+16+14+12+10

               Instruction base (button 1)
                  ____|____
                  |        |
1 01111101 01010101 10000000

Then the encoding is: 1011111010101010110000000
```

# SMC5326

Out of curiousity, I bought a SMC5326 from shopee and investigate it. I notice got two types of gate remote, one got DIP switches other one does not. The other one only duplicate the signal from old remote and transmit, and also cheaper.

[Shopee link](https://shopee.com.my/Auto-Gate-SMC5326-5326-330Mhz-433Mhz-8-Dip-Switch-Auto-Garage-Duplicate-Remote-Control-Duplicate-i.15599448.16265806043)

**DIP switch Remote**

![shopee](/uploads/gate/shopee.jpeg){: width="500" }

**Copy/Clone type Remote**

![shopee](/uploads/gate/shopee2.jpeg){: width="500" }

*After I get the remote, I set the same DIP switch as my home gate remote (UNILARM), surprisingly I can open my gate with the SMC5326 remote!*

I guess almost all gates remote uses the similar protocol as SMC5326, more convinient (also more dangerous because it is possible to open gates by only brute forcing)

# Implement Brute Force

Next I code a script to generate .sub files for brute forcing, I refering to a [github project](https://github.com/tobiabocchi/flipperzero-bruteforce) also generating brute forcing .sub files

It basically brute force all combinations of DIP switch. To narrow down the brute force time, it implements a technique like binary search (but need to play the signal multiple times)

Can refer to [my github repo](https://github.com/Hong5489/flipperzero-gate-bruteforce), if got Flipper Zero can test it out with your gate. 

When I try to brute force my gate, accidentally opens my neighbours gate 😂 **PS: Please test on your own gate or ask for permission**

# Conclusion

As Andre said, this type of remote control are widely found in Malaysia. It uses static codes, which is vulnerable to brute force and replay attack, so hope in future all our house gates can change it to rolling code to be more secure. Imagine anyone can open your house gate that is quite scary.. so if you are using this kind of remote for your gate, better change it to more secure one