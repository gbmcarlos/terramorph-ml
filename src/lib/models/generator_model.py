import torch.nn as nn
from .modules import ConvBlock, EncoderBlock, DecoderBlock


class Generator(nn.Module):
    def __init__(self, in_channels=3, out_channels=1):
        super().__init__()

        self.encoder_block_1 = EncoderBlock(in_channels, 64)
        self.encoder_block_2 = EncoderBlock(64, 128)
        self.encoder_block_3 = EncoderBlock(128, 256)
        self.encoder_block_4 = EncoderBlock(256, 512)

        self.bottle_neck_block = ConvBlock(512, 1024)

        self.decoder_block_1 = DecoderBlock(1024, 512)
        self.decoder_block_2 = DecoderBlock(512, 256)
        self.decoder_block_3 = DecoderBlock(256, 128)
        self.decoder_block_4 = DecoderBlock(128, 64)

        self.out_block = nn.Conv2d(in_channels=64, out_channels=out_channels, kernel_size=3, padding='same')

    def forward(self, x):

        convolved_1, encoded = self.encoder_block_1(x)
        convolved_2, encoded = self.encoder_block_2(encoded)
        convolved_3, encoded = self.encoder_block_3(encoded)
        convolved_4, encoded = self.encoder_block_4(encoded)

        encoded = self.bottle_neck_block(encoded)

        decoded = self.decoder_block_1(encoded, convolved_4)
        decoded = self.decoder_block_2(decoded, convolved_3)
        decoded = self.decoder_block_3(decoded, convolved_2)
        decoded = self.decoder_block_4(decoded, convolved_1)

        output = self.out_block(decoded)
        
        return output
