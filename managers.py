import config
from typing import List
from database import Database
from datetime import datetime


class HostelManager:
    def __init__(self):
        self.__db = Database(
            user=config.user,
            password=config.password,
            host=config.host,
            database=config.db_name
        )

    def get_service_report(self) -> List[dict]:
        return [{
            'doctor_surname': data[0],
            'doctor_name': data[1],
            'service_name': data[2],
            'cabinet': data[3]
        } for data in self.__db.select(
            table='documents.referral',
            fields=['doctor.surname', 'doctor.name', 'service.name', 'referral.cabinet'],
            joins=[
                ('persons.doctor', 'persons.doctor.id = documents.referral.doctor'),
                ('reference_info.service', 'referral.service = service.id'),
            ],
            order_by=[('documents.referral.appointment_time', 'DESC')],
            where="result = 'Услуга предоставлена'"
        )]

    def get_count_all_cases_of_diagnosis(self) -> List[dict]:
        return [{
            'diagnosis_id': data[0],
            'diagnosis_name': data[1],
            'count': data[2]
        } for data in self.__db.select(
            table='reference_info.diagnosis',
            fields=[
                'reference_info.diagnosis.id',
                'diagnosis.name',
                'count(conclusion.id) as referrals_count'
            ],
            joins=[
                ('documents.conclusion', 'documents.conclusion.diagnosis = diagnosis.id')
            ],
            group_by=['reference_info.diagnosis.id', 'diagnosis.name'],
            order_by=[('referrals_count', 'DESC')],
        )]

    def get_statistics_of_doctors_refferals(self) -> List[dict]:
        return [{
            'id': data[0],
            'surname': data[1],
            'name': data[2],
            'referrals_count': data[3]
        } for data in self.__db.select(
            table='persons.doctor',
            fields=[
                'doctor.id',
                'doctor.surname',
                'doctor.name',
                'count(referral.id) as referrals_count'
            ],
            joins=[('documents.referral', 'doctor.id = referral.doctor')],
            group_by=['doctor.id'],
            order_by=[('referrals_count', 'DESC')],
            having='count(referral.id) > 1'
        )]

    def get_hiled_diagnosis_for_period(self, start: datetime, end: datetime) -> List[dict]:
        return [{
            'diagnosis_name': data[0],
            'doctor_id': data[1],
            'registration_time': data[2],
        } for data in self.__db.select(
            table='documents.conclusion',
            fields=['diagnosis.name', 'doctor', 'registration_time'],
            joins=[('reference_info.diagnosis', 'diagnosis.id = conclusion.diagnosis')],
            group_by=['diagnosis.name', 'doctor', 'registration_time'],
            where=f"status = 'Вылечено' AND"
                  f" registration_time between '{start.isoformat()}' AND '{end.isoformat()}'"
        )]
