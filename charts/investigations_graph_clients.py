#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Module to produce Graph/s in relation to Investigations from InsightIDR for multiple clients"""

import json
from investigations_graph import client_counts,priority_counts
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import requests

