"""Test of pyModbusTCP.utils"""

import math
import unittest

from tecscipyModbusTCP.utils import (
    decode_ieee,
    encode_ieee,
    get_2comp,
    get_bits_from_int,
    get_list_2comp,
    int2bits,
    long_list_to_word,
    longs2words,
    twos_c,
    twos_c_l,
    word_list_to_long,
    words2longs,
)


class TestUtils(unittest.TestCase):
    """pyModbusTCP.utils function test class."""

    def test_get_bits_from_int(self):
        """Test function get_bits_from_int and it's short alias int2bits."""
        # default bits list size is 16
        self.assertEqual(len(get_bits_from_int(0)), 16)
        # for 8 size (positional arg)
        self.assertEqual(len(get_bits_from_int(0, 8)), 8)
        # for 32 size (named arg)
        self.assertEqual(len(get_bits_from_int(0, val_size=32)), 32)
        # test binary decode
        self.assertEqual(int2bits(0x0000), [False] * 16)
        self.assertEqual(int2bits(0xFFFF), [True] * 16)
        self.assertEqual(int2bits(0xF007), [True] * 3 + [False] * 9 + [True] * 4)
        self.assertEqual(int2bits(6, 4), [False, True, True, False])

    def test_ieee(self):
        """Test IEEE functions: decode_ieee and encode_ieee."""
        # test IEEE NaN
        self.assertTrue(math.isnan(decode_ieee(0x7FC00000)))
        self.assertEqual(encode_ieee(float("nan")), 0x7FC00000)
        # test +/- infinity
        self.assertTrue(math.isinf(decode_ieee(0xFF800000)))
        self.assertTrue(math.isinf(decode_ieee(0x7F800000)))
        # test big and small values
        avogad = 6.022140857e23
        avo_32 = 0x66FF0C2F
        avo_64 = 0x44DFE185D2F54B67
        planck = 6.62606957e-34
        pla_32 = 0x085C305E
        pla_64 = 0x390B860BB596A559
        # IEEE single or double precision format -> float
        self.assertAlmostEqual(decode_ieee(avo_32), avogad, delta=avogad * 1e-7)
        self.assertAlmostEqual(decode_ieee(avo_64, double=True), avogad)
        self.assertAlmostEqual(decode_ieee(pla_32), planck)
        self.assertAlmostEqual(decode_ieee(pla_64, double=True), planck)
        # float -> IEEE single or double precision format
        self.assertAlmostEqual(encode_ieee(avogad), avo_32)
        self.assertAlmostEqual(encode_ieee(avogad, double=True), avo_64)
        self.assertAlmostEqual(encode_ieee(planck), pla_32)
        self.assertAlmostEqual(encode_ieee(planck, double=True), pla_64)

    def test_word_list_to_long(self):
        """Test function word_list_to_long and it 's short alias words2longs."""
        # empty list, return empty list
        self.assertEqual(word_list_to_long([]), [])
        # if len of list is odd ignore last value
        self.assertEqual(word_list_to_long([0x1, 0x2, 0x3]), [0x10002])
        # test convert with big and little endian
        l1 = [0xDEAD, 0xBEEF]
        l2 = [0xFEED, 0xFACE, 0xCAFE, 0xBEEF]
        big = dict(big_endian=True)
        nobig = dict(big_endian=False)
        big64 = dict(big_endian=True, long_long=True)
        nobig64 = dict(big_endian=False, long_long=True)
        self.assertEqual(words2longs(l1, **big), [0xDEADBEEF])
        self.assertEqual(words2longs(l2, **big), [0xFEEDFACE, 0xCAFEBEEF])
        self.assertEqual(words2longs(l1, **nobig), [0xBEEFDEAD])
        self.assertEqual(words2longs(l2, **nobig), [0xFACEFEED, 0xBEEFCAFE])
        self.assertEqual(words2longs(l1 * 2, **big64), [0xDEADBEEFDEADBEEF])
        self.assertEqual(words2longs(l2 * 2, **big64), [0xFEEDFACECAFEBEEF] * 2)
        self.assertEqual(words2longs(l1 * 2, **nobig64), [0xBEEFDEADBEEFDEAD])
        self.assertEqual(words2longs(l2 * 2, **nobig64), [0xBEEFCAFEFACEFEED] * 2)

    def test_long_list_to_word(self):
        """Test function long_list_to_word and short alias longs2words."""
        # empty list, return empty list
        self.assertEqual(long_list_to_word([]), [])
        # test convert with big and little endian
        l1 = [0xDEADBEEF]
        l1_big = [0xDEAD, 0xBEEF]
        l1_nobig = [0xBEEF, 0xDEAD]
        l1_big64 = [0x0000, 0x0000, 0xDEAD, 0xBEEF]
        l1_nobig64 = [0xBEEF, 0xDEAD, 0x0000, 0x0000]
        l2 = [0xFEEDFACE, 0xCAFEBEEF]
        l2_big = [0xFEED, 0xFACE, 0xCAFE, 0xBEEF]
        l2_nobig = [0xFACE, 0xFEED, 0xBEEF, 0xCAFE]
        l3 = [0xFEEDFACECAFEBEEF]
        l3_big64 = [0xFEED, 0xFACE, 0xCAFE, 0xBEEF]
        l3_nobig64 = [0xBEEF, 0xCAFE, 0xFACE, 0xFEED]
        big = dict(big_endian=True)
        nobig = dict(big_endian=False)
        big64 = dict(big_endian=True, long_long=True)
        nobig64 = dict(big_endian=False, long_long=True)
        self.assertEqual(longs2words(l1, **big), l1_big)
        self.assertEqual(longs2words(l2, **big), l2_big)
        self.assertEqual(longs2words(l1, **nobig), l1_nobig)
        self.assertEqual(longs2words(l2, **nobig), l2_nobig)
        self.assertEqual(longs2words(l1 * 2, **big64), l1_big64 * 2)
        self.assertEqual(longs2words(l3 * 2, **big64), l3_big64 * 2)
        self.assertEqual(longs2words(l1 * 4, **nobig64), l1_nobig64 * 4)
        self.assertEqual(longs2words(l3 * 4, **nobig64), l3_nobig64 * 4)

    def test_get_2comp(self):
        """Test function get_2comp and it's short alias twos_c."""
        # check if ValueError exception is raised
        self.assertRaises(ValueError, get_2comp, 0x10000)
        self.assertRaises(ValueError, get_2comp, -0x8001)
        self.assertRaises(ValueError, twos_c, 0x100000000, val_size=32)
        self.assertRaises(ValueError, twos_c, -0x80000001, val_size=32)
        # 2's complement of 16bits values (default)
        self.assertEqual(get_2comp(0x0001), 0x0001)
        self.assertEqual(get_2comp(0x8000), -0x8000)
        self.assertEqual(get_2comp(-0x8000), 0x8000)
        self.assertEqual(get_2comp(0xFFFF), -0x0001)
        self.assertEqual(get_2comp(-0x0001), 0xFFFF)
        self.assertEqual(get_2comp(-0x00FA), 0xFF06)
        self.assertEqual(get_2comp(0xFF06), -0x00FA)
        # 2's complement of 32bits values
        self.assertEqual(twos_c(0xFFFFFFF, val_size=32), 0xFFFFFFF)
        self.assertEqual(twos_c(-1, val_size=32), 0xFFFFFFFF)
        self.assertEqual(twos_c(0xFFFFFFFF, val_size=32), -1)
        self.assertEqual(twos_c(125, val_size=32), 0x0000007D)
        self.assertEqual(twos_c(0x0000007D, val_size=32), 125)
        self.assertEqual(twos_c(-250, val_size=32), 0xFFFFFF06)
        self.assertEqual(twos_c(0xFFFFFF06, val_size=32), -250)
        self.assertEqual(twos_c(0xFFFEA2A5, val_size=32), -89435)
        self.assertEqual(twos_c(-89435, val_size=32), 0xFFFEA2A5)

    def test_get_list_2comp(self):
        """Test get_list_2comp and it's short alias twos_c_l."""
        self.assertEqual(get_list_2comp([0x8000], 16), [-32768])
        in_l = [0x8000, 0xFFFF, 0x0042]
        out_l = [-0x8000, -0x0001, 0x42]
        self.assertEqual(twos_c_l(in_l, val_size=16), out_l)
        in_l = [0x8000, 0xFFFFFFFF, 0xFFFEA2A5]
        out_l = [0x8000, -0x0001, -89435]
        self.assertEqual(twos_c_l(in_l, val_size=32), out_l)


if __name__ == "__main__":
    unittest.main()
