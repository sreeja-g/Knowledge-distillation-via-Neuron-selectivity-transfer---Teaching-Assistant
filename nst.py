from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import torch
import torch.nn as nn
import torch.nn.functional as F

class NST(nn.Module):
	def __init__(self):
		super(NST, self).__init__()

	def forward(self, fm_s, fm_t):
   
		fm_s = fm_s.view(fm_s.size(0), fm_s.size(1), -1)
		fm_s = F.normalize(fm_s, dim=2)

		avg_pool = nn.AdaptiveAvgPool1d(fm_s.size(0))
		fm_t = fm_t.view(-1, fm_t.size(1), fm_t.size(0))
		fm_t = avg_pool(fm_t)

		fm_t = fm_t.view(-1, fm_t.size(1), fm_t.size(0))
		fm_t = F.normalize(fm_t, dim=2)

		loss = self.poly_kernel(fm_t, fm_t).mean() \
			 + self.poly_kernel(fm_s, fm_s).mean() \
			 - 2 * self.poly_kernel(fm_s, fm_t).mean()

		return loss

	def poly_kernel(self, fm1, fm2):
		fm1 = fm1.unsqueeze(1)
		fm2 = fm2.unsqueeze(2)
		out = (fm1 * fm2).sum(-1).pow(2)

		return out
