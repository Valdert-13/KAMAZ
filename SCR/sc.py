import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_percentage_error
from fbprophet import Prophet
from tqdm import tqdm
tqdm.pandas()
pd.set_option('display.max_columns', None)


class Generator_df:
    """
    Класс создания датафремов на основании Prophet

    Parameters
    ----------

     df: pd.DataFrame
        датасет содержащий поле date

    period: int
        Число точек времянного ряда для валидации.


    year: int
        Год с которого начинается времянной ряд.

    """

    def __init__(self,
                 df: pd.DataFrame,
                 period: int = 12,
                 year: int = 2009):

        self.df = df
        self.period = period
        self.year = year
        self.result = self._pred_prophet()

    def _pred_prophet(self):
        """
        Валидация для модели Prophet.


        Returns
        -------
        result: dict.
            key - имя столбца (за исключением date)
            value - dict {mape: ошибка mape
                          data: df с предсказаниями}

        """

        result = {}

        list_cols = self.df.columns.to_list()
        list_cols.remove('date')

        data = self.df.loc[self.df['date'].dt.year >= self.year]

        for col in tqdm(list_cols):
            model = Prophet(daily_seasonality=False,
                            weekly_seasonality=False,
                            yearly_seasonality=False,
                            interval_width=0.95
                            ).add_seasonality(
                name='yearly', period=365.25, fourier_order=6
            )

            df_1 = data[['date', col]]
            df_1.columns = ['ds', 'y']
            df_1 = df_1.loc[df_1['y'].isna() == False]
            data_train = df_1[:self.period * -1]
            data_test = df_1[self.period * -1:]
            model.fit(data_train)
            future = model.make_future_dataframe(periods=self.period, freq='MS')  # test data count
            forecast = model.predict(future)
            mape = mean_absolute_percentage_error(forecast['yhat'][self.period * -1:], data_test['y'])

            month = int((data.date.iloc[-1] - df_1.ds.iloc[-1]) / np.timedelta64(1, 'M'))

            future = model.make_future_dataframe(periods=self.period * 2 + month, freq='MS')
            forecast = model.predict(future)
            forecast['up'] = forecast['yhat_upper'] - forecast['yhat']
            forecast['down'] = forecast['yhat_lower'] - forecast['yhat']
            result[col] = {'mape': mape, 'data': forecast}

        return result

    def data_gen(self, mape: float = 0.16, params: dict = {}):
        """
        Создание датасета на основании предсказаних Prophet.

        Parameters
        ----------
        mape: float.
            проходной уровень ошибки.


        params: dict
            Словарь с параметрами для фичей


        Returns
        -------
        df_result: pd.DataFrame
            возвращает созданный датафрем с учетом переданных параметров




        """

        df = self._add_12_months()

        df_result = df.copy()

        list_cols = df.columns.to_list()
        list_cols.remove('date')
        names_params = params.keys()
        for col in list_cols:
            random = 1
            if self.result[col]['mape'] < mape:

                if col in names_params:
                    trent = params[col]['trend']
                    df_result = df_result.merge(self.result[col]['data'][['ds', 'yhat', trent]], \
                                                how="left", left_on="date", right_on='ds')

                    df_result['yhat'] = df_result[trent] * params[col]['change'] * random + df_result['yhat']

                    df_result.loc[df_result[col].isna() == True, col] = df_result['yhat']
                    df_result = df_result.drop(['ds', 'yhat', trent], axis=1)

                else:
                    df_result = df_result.merge(self.result[col]['data'][['ds', 'yhat']], how="left", \
                                                left_on="date", right_on='ds')
                    df_result.loc[df_result[col].isna() == True, col] = df_result['yhat']
                    df_result = df_result.drop(['ds', 'yhat'], axis=1)



            else:
                if col in names_params:
                    if params[col]['trend'] == 'down':
                        trend = -1
                    elif params[col]['trend'] == 'up':
                        trend = 1
                    value = df_result.loc[df_result[col].isna() == False][col].iloc[-1]

                    if params[col]['type_change'] == 'linear':
                        value = value + value * params[col]['change'] * trend  # По рандому вопрос
                        df_result.iloc[-1, df_result.columns.get_loc(col)] = value
                        df_result[col] = df_result[col].interpolate()


                    elif params[col]['type_change'] == 'even':
                        value = value + value * params[col]['change'] * trend  # По рандому вопрос
                        df_result[col] = df_result[col].fillna(value)


                else:
                    df_result[col] = df[col].fillna(method='ffill')

        return df_result[-1 * self.period:]

    def _add_12_months(self):
        df = self.df.append(pd.DataFrame({'date': pd.date_range(start=self.df.date.iloc[-1],
                                                                periods=self.period, freq='MS',
                                                                closed='right')})).reset_index(drop=True)
        return df