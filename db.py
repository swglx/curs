import psycopg2
class RegDB:
    def __init__(self, db_file):
        """Инициализация соединения с БД"""
        self.conn = psycopg2.connect(
            host="localhost",
            database="registratura",
            user="postgres",
            password="root"
        )
        self.cursor = self.conn.cursor()

        self.check_connection()

    def check_connection(self):
            """Проверка подключения к базе данных"""
            try:
                if self.conn.closed == 0:
                    print("Подключение к базе данных установлено.")
                else:
                    print("Не удалось установить подключение к базе данных.")
            except psycopg2.Error as e:
                print(f"Ошибка при проверке подключения к базе данных: {e}")

    def login_db(self, login, password):
        """Проверка логина и пароля пользователя"""
        try:
            query = 'SELECT * FROM "users" WHERE "log" = %s AND "password" = %s'
            self.cursor.execute(query, (login, password))
            user = self.cursor.fetchone()  # Получаем одну запись

            if user:
                return True  # Пользователь найден
            else:
                return False  # Пользователь не найден
        except Exception as e:
            print(f"Ошибка при проверке логина и пароля: {e}")
            return False

    def get_users(self):
        try:
            """Вывод пользователей из БД"""
            query = "SELECT us_id, log, password FROM users"
            self.cursor.execute(query)
            users = self.cursor.fetchall()
            return users
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def add_user(self, log, password):
        try:
            query = "INSERT INTO users (log, password) VALUES (%s, %s)"
            values = (log, password)
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def delete_user(self, user_id):
        try:
            query = "DELETE FROM users WHERE us_id = %s"
            self.cursor.execute(query, (user_id,))
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False
    def get_diagnoses(self):
        try:
            """Вывод диагнозов из БД"""
            query = "SELECT diag_id, code, special, recovery_time, diagnos FROM diagnoses "
            self.cursor.execute(query)
            diagnoses = self.cursor.fetchall()
            return diagnoses
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def add_dg(self, code, special, rec_time, dg):
        try:
            query = "INSERT INTO diagnoses (code, special, recovery_time, diagnos) VALUES (%s, %s, %s,%s)"
            values = (code, special, rec_time, dg)
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def delete_dg_from_db(self, num):
        try:
            query = "DELETE FROM diagnoses WHERE diag_id = %s"
            self.cursor.execute(query, (num,))
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def get_cabinets(self):
        try:
            """Вывод кабинетов из БД"""
            query = "SELECT cabinet_id,number, description FROM cabinet "
            self.cursor.execute(query)
            cabinets = self.cursor.fetchall()
            return cabinets
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def add_cabinet(self, num,desc):
        try:
            query = "INSERT INTO cabinet (number, description) VALUES (%s, %s)"
            values = (num, desc)
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def delete_cabinet_from_db(self, number):
        try:
            query = "DELETE FROM cabinet WHERE number = %s"
            self.cursor.execute(query, (number,))
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False


    def get_doctors(self):
        try:
            query = """
                SELECT d.doc_id, d.doc_name, d.doc_surname, d.doc_midname, c.number, sp.spec_description
                FROM doctor d
                JOIN cabinet c ON d.cabinet_id = c.cabinet_id
                JOIN specialization s ON s.doc_id = d.doc_id
                JOIN specialty sp ON sp.spec_id = s.spec_id
            """
            self.cursor.execute(query)
            doctors = self.cursor.fetchall()
            return doctors
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def add_doctor(self, name, surname, midname, cabinet, dsp, place, date):
        try:
            # Вставка записи в таблицу "doctor" и получение doc_id
            query = "INSERT INTO doctor (doc_name, doc_surname, doc_midname, cabinet_id) VALUES (%s, %s, %s, %s) RETURNING doc_id"
            values = (name, surname, midname, cabinet)
            self.cursor.execute(query, values)
            doc_id = self.cursor.fetchone()[0]
            self.conn.commit()

            # Вставка записи в таблицу "specialization"
            query = "INSERT INTO specialization (doc_id, spec_id, place_rec, date_rec) VALUES (%s, %s, %s, %s)"
            values = (doc_id, dsp, place, date)
            self.cursor.execute(query, values)
            self.conn.commit()

            return True
        except:
            self.conn.rollback()
            return False

    def delete_doctor_from_db(self, doc):
        try:
            # Удаление записей из таблицы "specialization" по doc_id
            query = "DELETE FROM specialization WHERE doc_id = %s"
            self.cursor.execute(query, (doc,))

            # Удаление записи из таблицы "doctor"
            query = "DELETE FROM doctor WHERE doc_id = %s"
            self.cursor.execute(query, (doc,))

            return True
        except:
            # Откат транзакции в случае ошибки
            self.conn.rollback()
            return False

    def get_plots(self):
         try:
                """Вывод участков из БД"""
                query = "SELECT plot_id, address_list FROM plots "
                self.cursor.execute(query)
                plot = self.cursor.fetchall()
                return plot
         except Exception as e:
                print(f"An error occurred: {e}")
                return []

    def add_plot(self, adr):
        try:
            query = "INSERT INTO plots (address_list) VALUES ( %s)"
            values = (adr,)
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def delete_plot_from_db(self, num):
        try:
            query = "DELETE FROM plots WHERE plot_id = %s "
            self.cursor.execute(query, (num,))
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def get_carts(self):
        try:
            """Вывод врачей из БД"""
            query = "SELECT patient_id, policy_number, plot_id, pat_name, pat_surname, pat_midname, address, work_place, complaints FROM patientcard ORDER BY patient_id ASC "
            self.cursor.execute(query)
            cart = self.cursor.fetchall()
            return cart
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def add_patient(self, plot_id, policynumb, name, surname, midname, address, work_place, complaints):
        try:
            query = "INSERT INTO patientcard (plot_id, policy_number, pat_name, pat_surname, pat_midname, address, work_place, complaints) VALUES (%s, %s, %s,%s, %s, %s, %s, %s)"
            values = (plot_id, policynumb, name, surname, midname, address, work_place, complaints)
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def delete_patient_from_db(self, name):
        try:
            query = "DELETE FROM patientcard WHERE pat_name = %s "
            self.cursor.execute(query, (name,))
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def update_patient(self, pol_numb, new_id, new_surname, new_address, new_work, new_complaints):
        try:
            if pol_numb:
                query = "UPDATE patientcard SET policy_number = %s WHERE policy_number = %s"
                self.cursor.execute(query, (pol_numb, pol_numb))
                self.conn.commit()
            if new_id:
                query = "UPDATE patientcard SET plot_id = %s WHERE policy_number = %s"
                self.cursor.execute(query, (new_id, pol_numb))
                self.conn.commit()
            if new_surname:
                query = "UPDATE patientcard SET pat_surname = %s WHERE policy_number = %s"
                self.cursor.execute(query, (new_surname, pol_numb))
                self.conn.commit()
            if new_address:
                query = "UPDATE patientcard SET address = %s WHERE policy_number = %s"
                self.cursor.execute(query, (new_address, pol_numb))
                self.conn.commit()
            if new_work:
                query = "UPDATE patientcard SET work_place = %s WHERE policy_number = %s"
                self.cursor.execute(query, (new_work, pol_numb))
                self.conn.commit()
            if new_complaints:
                query = "UPDATE patientcard SET complaints = %s WHERE policy_number = %s"
                self.cursor.execute(query, (new_complaints, pol_numb))
                self.conn.commit()
            return "Информация о пациенте успешно обновлена!"
        except Exception as e:
            return f"Произошла ошибка при обновлении информации о пациенте: {e}"


    def get_sick(self):
        try:
            """Вывод врачей из БД"""
            query = """
                SELECT s.sick_id, pc.pat_surname, dr.doc_surname, s.date_issue, s.date_closing
                FROM sickleave s
                JOIN patientcard pc ON s.patient_id = pc.patient_id
                JOIN doctor dr ON s.doc_id = dr.doc_id
            """
            self.cursor.execute(query)
            sick = self.cursor.fetchall()
            return sick
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def add_sick(self, pat, doc, date_open, date_close, diag, date_diag):
        try:
            # Вставка записи в таблицу "sickleave" и получение sick_id
            query = "INSERT INTO sickleave (doc_id, patient_id, date_issue, date_closing) VALUES (%s, %s, %s, %s) RETURNING sick_id, doc_id"
            values = (doc, pat, date_open, date_close)
            self.cursor.execute(query, values)
            row = self.cursor.fetchone()
            sick_id = row[0]
            doc_id = row[1]
            self.conn.commit()

            # Вставка записи в таблицу "dsickleave"
            query = "INSERT INTO dsickleave (sick_id, doc_id, diag_id, date_diag) VALUES (%s, %s, %s, %s)"
            values = (sick_id, doc_id, diag, date_diag)
            self.cursor.execute(query, values)
            self.conn.commit()

            return True
        except:
            self.conn.rollback()

            return False

    def delete_sick_from_db(self, sick):
        try:
            # Удаление записей из таблицы "dsickleave" по doc_id
            query = "DELETE FROM dsickleave WHERE sick_id = %s"
            self.cursor.execute(query, (sick,))

            # Удаление записи из таблицы "sickleave"
            query = "DELETE FROM sickleave WHERE sick_id = %s"
            self.cursor.execute(query, (sick,))

            return True
        except:
            # Откат транзакции в случае ошибки
            self.conn.rollback()
            return False

    def get_dispensary(self):
        try:
            """Вывод врачей из БД"""
            query = """
                SELECT d.disp_id, pc.pat_surname, dr.doc_surname, di.diagnos, d.date_appear
                FROM dispensary d
                JOIN patientcard pc ON d.patient_id = pc.patient_id
                JOIN doctor dr ON d.doc_id = dr.doc_id
                JOIN diagnoses di ON d.diag_id = di.diag_id
            """
            self.cursor.execute(query)
            disp = self.cursor.fetchall()
            return disp
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def add_dispensary(self, pat, doc, date, diag):
        try:
            query = "INSERT INTO dispensary (patient_id, doc_id, diag_id, date_appear) VALUES (%s, %s, %s, %s)"
            values = (pat, doc, diag, date)
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def delete_disp_from_db(self,  disp):
        try:
            query = "DELETE FROM dispensary WHERE disp_id = %s "
            self.cursor.execute(query, (disp,))
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def get_home(self):
        try:
            query = """
                SELECT hs.home_id, d.doc_surname, pc.pat_surname, hs.date_service FROM homeservice hs
                JOIN doctor d ON hs.doc_id = d.doc_id
                JOIN patientcard pc ON hs.patient_id = pc.patient_id
            """
            self.cursor.execute(query)
            hm = self.cursor.fetchall()
            return hm
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def add_home(self, pat, doc, date):
        try:
            query = "INSERT INTO homeservice (doc_id, patient_id, date_service) VALUES (%s, %s, %s)"
            values = (doc, pat, date)
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def delete_home_from_db(self,  home):
        try:
            query = "DELETE FROM homeservice WHERE home_id = %s "
            self.cursor.execute(query, (home,))
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def get_clinic(self):
        try:
            query = """
                SELECT c.clinic_id, pc.pat_surname, d.doc_surname, k.number, c.date_visit, c.reception, c.appointments
                FROM clinicservice c
                JOIN patientcard pc ON c.patient_id = pc.patient_id
                JOIN doctor d ON c.doc_id = d.doc_id
                JOIN cabinet k ON c.cabinet_id = k.cabinet_id
                ORDER BY c.clinic_id ASC
            """
            self.cursor.execute(query)
            cl = self.cursor.fetchall()
            return cl
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def add_clinic(self, pat, doc, cab, date, rec, app):
        try:
            query = "INSERT INTO clinicservice (patient_id, doc_id, cabinet_id, date_visit, reception, appointments) VALUES (%s, %s, %s,%s, %s, %s)"
            values = (pat, doc, cab, date, rec, app)
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def delete_clinic_from_db(self,  clinic):
        try:
            query = "DELETE FROM clinicservice WHERE clinic_id = %s "
            self.cursor.execute(query, (clinic,))
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def update_clinic(self, clinic_id, new_rec):
        try:
            if clinic_id and new_rec:
                query = "UPDATE clinicservice SET reception = %s WHERE clinic_id = %s"
                self.cursor.execute(query, (new_rec, clinic_id))
                self.conn.commit()
                return "Информация о приёме успешно обновлена!"
            else:
                return "Некорректные данные для обновления приёма."
        except Exception as e:
            return f"Произошла ошибка при обновлении информации о приёме: {e}"

    def get_dsp(self):
        try:
            """Вывод специальностей из БД"""
            query = "SELECT spec_id,spec_description FROM specialty "
            self.cursor.execute(query)
            ds = self.cursor.fetchall()
            return ds
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def add_specialty(self, spec_description):
        try:
            query = "INSERT INTO specialty (spec_description) VALUES (%s)"
            values = (spec_description,)
            self.cursor.execute(query, values)
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def delete_specialty_from_db(self, spec_description):
        try:
            query = "DELETE FROM specialty WHERE spec_description = %s"
            self.cursor.execute(query, (spec_description,))
            self.conn.commit()
            return True
        except:
            self.conn.rollback()
            return False

    def get_spec(self):
        try:
            query = """
                SELECT d.doc_surname, sp.spec_description, s.place_rec, s.date_rec
                FROM specialization s
                JOIN doctor d ON d.doc_id = s.doc_id
                JOIN specialty sp ON sp.spec_id = s.spec_id
            """
            self.cursor.execute(query)
            sp = self.cursor.fetchall()
            print(sp)
            return sp
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def get_dsk(self):
        try:
            query = """
                SELECT dsl.sick_id, d.doc_surname, dg.diagnos, dsl.date_diag
                FROM dsickleave dsl
                JOIN doctor d ON d.doc_id = dsl.doc_id
                JOIN diagnoses dg ON dg.diag_id = dsl.diag_id
            """
            self.cursor.execute(query)
            ds = self.cursor.fetchall()
            return ds
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

