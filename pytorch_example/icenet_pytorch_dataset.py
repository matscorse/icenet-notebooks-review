from __future__ import annotations

import pandas as pd
from icenet.data.dataset import IceNetDataSet
from torch.utils.data import Dataset

class IceNetDataSetPyTorch(Dataset):
    def __init__(self,
                 configuration_path: str,
                 mode: str,
                 n_forecast_days: int | None = None,
                 generate_workers: int | None = None):
        self._ds = IceNetDataSet(configuration_path=configuration_path)
        self._dl = self._ds.get_data_loader(
            n_forecast_days=n_forecast_days,
            generate_workers=generate_workers
        )
                
        # check mode option
        if mode not in ["train", "val", "test"]:
            raise ValueError("mode must be either 'train', 'val' or 'test'")
        self._mode = mode
        
        self._dates = [
            x.replace('_', '-')
            for x in self._dl._config["sources"]["osisaf"]["dates"][self._mode]
        ]
    
    def __len__(self):
        return self._ds._counts[self._mode]
    
    def __getitem__(self, idx):
        return self._dl.generate_sample(date=pd.Timestamp(self._dates[idx]))