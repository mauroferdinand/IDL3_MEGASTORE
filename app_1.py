import streamlit as st
from supabase import create_client, Client

# Conexión a Supabase
url = "https://wyxknkpsaabzgzcpysmg.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind5eGtua3BzYWFiemd6Y3B5c21nIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjM5MzUyNDIsImV4cCI6MjAzOTUxMTI0Mn0.4WpnRjGHbKZT6lhVoMdLDlI_gaYCVp8Jc8B685-4llU"
supabase: Client = create_client(url, key)

def get_users():
    response = supabase.table('users').select('*').execute()
    return response.data

# Mostrar la tabla
def display_users(users):
    st.table(users)

if __name__ == "__main__":
    st.title("CRUD con Streamlit y Supabase")
    
    users = get_users()
    display_users(users)

# Formulario para crear un nuevo usuario
st.header("Agregar un nuevo usuario")

with st.form("user_form"):
    name = st.text_input("Nombre")
    email = st.text_input("Email")
    submit = st.form_submit_button("Agregar")

    if submit:
        supabase.table('users').insert({"name": name, "email": email}).execute()
        st.success("Usuario agregado exitosamente")

# Edición de usuario
def update_user(user_id, new_name, new_email):
    supabase.table('users').update({"name": new_name, "email": new_email}).eq("id", user_id).execute()

if "edit_id" not in st.session_state:
    st.session_state["edit_id"] = None

if st.session_state["edit_id"]:
    user = supabase.table('users').select('*').eq('id', st.session_state["edit_id"]).execute().data[0]
    st.header(f"Editando usuario: {user['name']}")

    with st.form("edit_form"):
        name = st.text_input("Nombre", user['name'])
        email = st.text_input("Email", user['email'])
        submit = st.form_submit_button("Actualizar")

        if submit:
            update_user(st.session_state["edit_id"], name, email)
            st.success("Usuario actualizado exitosamente")
            st.session_state["edit_id"] = None
else:
    # Mostrar usuarios con opción de editar
    users = get_users()
    for user in users:
        if st.button(f"Editar {user['name']}"):
            st.session_state["edit_id"] = user['id']

# Eliminar un usuario
def delete_user(user_id):
    supabase.table('users').delete().eq('id', user_id).execute()

if "delete_id" not in st.session_state:
    st.session_state["delete_id"] = None

for user in users:
    if st.button(f"Eliminar {user['name']}"):
        delete_user(user['id'])
        st.success(f"Usuario {user['name']} eliminado exitosamente")
