Running solve.py will bruteforce the hashes. They were sorted by image size, using the product of width and height as heuristic:

```
(400, 433) - 602a4a8fff652291fdc0e049e3900dae608af64e5e4d2c5d4332603c9938171d. Product: 173200
(465, 464) - 372df01b994c2b14969592fd2e78d27e7ee472a07c7ac3dfdf41d345b2f8e305. Product: 215760
(525, 489) - 70f87d0b880efcdbe159011126db397a1231966991ae9252b278623aeb9c0450. Product: 256725
(512, 512) - aa105295e25e11c8c42e4393c008428d965d42c6cb1b906e30be99f94f473bb5. Product: 262144
(559, 530) - f40e838809ddaa770428a4b2adc1fff0c38a84abe496940d534af1232c2467d5. Product: 296270
(513, 613) - 456ae6a020aa2d54c0c00a71d63033f6c7ca6cbc1424507668cf54b80325dc01. Product: 314469
(585, 577) - 77a39d581d3d469084686c90ba08a5fb6ce621a552155730019f6c02cb4c0cb6. Product: 337545
(598, 605) - bd0fd461d87fba0d5e61bed6a399acdfc92b12769f9b3178f9752e30f1aeb81d. Product: 361790
```

Sorting the files:
```
508K    File5_encr.ppm
636K    File7_encr.ppm
756K    File4_encr.ppm
772K    File1_encr.ppm
868K    File8_encr.ppm
924K    File6_encr.ppm
992K    File3_encr.ppm
1.1M    File2_encr.ppm
```

Correlating the hashes with the files, given the order in the sortings:

```
File5_encr.ppm - 602a4a8fff652291fdc0e049e3900dae608af64e5e4d2c5d4332603c9938171d
File7_encr.ppm - 372df01b994c2b14969592fd2e78d27e7ee472a07c7ac3dfdf41d345b2f8e305
File4_encr.ppm - 70f87d0b880efcdbe159011126db397a1231966991ae9252b278623aeb9c0450
File1_encr.ppm - aa105295e25e11c8c42e4393c008428d965d42c6cb1b906e30be99f94f473bb5
File8_encr.ppm - f40e838809ddaa770428a4b2adc1fff0c38a84abe496940d534af1232c2467d5
File6_encr.ppm - 456ae6a020aa2d54c0c00a71d63033f6c7ca6cbc1424507668cf54b80325dc01
File3_encr.ppm - 77a39d581d3d469084686c90ba08a5fb6ce621a552155730019f6c02cb4c0cb6
File2_encr.ppm - bd0fd461d87fba0d5e61bed6a399acdfc92b12769f9b3178f9752e30f1aeb81d
```
