#!/usr/bin/env python3
"""Small exact parser regression; no large chart construction is performed."""
from fractions import Fraction as Q
import base64
import copy
import hashlib
import struct
import unittest
import zlib

from build_endpoint_tail_charts import Field


def fixture():
    values = [4, 2, 4, 2, 4]
    raw = struct.pack('<5I', *values)
    compact = {
        'format': 'qout-clock-grid-field-u32-zlib-v1',
        'n': 1, 'field_denominator': '4',
        'encoding': {
            'count': 5, 'integer_type': 'uint32 little-endian',
            'compression': 'zlib',
            'uncompressed_sha256': hashlib.sha256(raw).hexdigest(),
        },
        'pre_two_values_base64': base64.b64encode(zlib.compress(raw)).decode(),
    }
    legacy = {
        'n': 1, 'cdf_denominator': '4',
        'radial_nodal': [[0, 2, 4], [1, 1, 2], [2, 2, 4],
                         [3, 1, 2], [4, 2, 4]],
    }
    strategy = {
        'format': 'normalized-qout-princess-p1-v1',
        'n': 1, 'cdf_denominator': '4',
        'interpolation_epsilon': '1/512',
        'nodal_profile': compact,
    }
    return compact, legacy, strategy


class ParserTests(unittest.TestCase):
    def test_formats_and_explicit_width(self):
        compact, legacy, strategy = fixture()
        for epsilon in (Q(1, 2), Q(1, 4)):
            fields = [Field(data, epsilon) for data in (compact, legacy, strategy)]
            self.assertTrue(all(field.pre == fields[0].pre for field in fields))
            self.assertTrue(all(field.epsilon == epsilon for field in fields))
            for t, x in ((Q(0), Q(1, 3)), (Q(1, 2), Q(-1, 4)),
                         (Q(7, 4), Q(3, 4)), (Q(5, 2), Q(3, 4))):
                self.assertTrue(all(field.cdf(t, x) == fields[0].cdf(t, x)
                                    for field in fields))
        # The saved strategy width is not implicitly imported.
        self.assertEqual(Field(strategy).epsilon, Q(1, 2))

    def test_wrapper_metadata(self):
        _, _, original = fixture()
        changes = [
            lambda d: d.update(n=2),
            lambda d: d.update(cdf_denominator='5'),
            lambda d: d.update(field_denominator='5'),
            lambda d: d.pop('cdf_denominator'),
            lambda d: d.pop('nodal_profile'),
            lambda d: d.update(n=True),
            lambda d: d.update(cdf_denominator=4.0),
            lambda d: d['nodal_profile'].update(n='1.0'),
            lambda d: d['nodal_profile'].update(cdf_denominator='5'),
            lambda d: d['nodal_profile'].update(format='normalized-qout-princess-p1-v1'),
        ]
        for change in changes:
            data = copy.deepcopy(original)
            change(data)
            with self.subTest(data=data):
                with self.assertRaises((ValueError, KeyError, AssertionError)):
                    Field(data)

    def test_payload_validation_is_not_bypassed(self):
        _, _, original = fixture()
        changes = [
            lambda d: d['nodal_profile']['encoding'].update(count=4),
            lambda d: d['nodal_profile']['encoding'].update(uncompressed_sha256='0'*64),
            lambda d: d['nodal_profile'].update(field_denominator='3'),
        ]
        for change in changes:
            data = copy.deepcopy(original)
            change(data)
            with self.assertRaises((ValueError, AssertionError)):
                Field(data)
        compact, _, _ = fixture()
        compact['field_denominator'] = '3'
        with self.assertRaises(AssertionError):
            Field(compact)  # A decoded node exceeds the declared scale.


if __name__ == '__main__':
    unittest.main()
