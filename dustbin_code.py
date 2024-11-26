@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        patients = load_patients()

        if email not in patients:
            flash('Invalid email address!', 'danger')
            return redirect(url_for('forgot_password'))

        token = serializer.dumps(email, salt='password-reset-salt')
        reset_url = url_for('reset_password', token=token, _external=True)
        msg = Message('Password Reset Request', sender='your_email@example.com', recipients=[email])
        msg.body = f'Please click the link to reset your password: {reset_url}'

        try:
            logging.debug(f'Sending email to {email} with reset link: {reset_url}')
            mail.send(msg)
            flash('Password reset link sent to your email.', 'info')
        except socket.gaierror as e:
            logging.error(f'Failed to connect to the email server: {e}')
            flash('Failed to connect to the email server. Please check your network and email server configuration.', 'danger')
        except Exception as e:
            logging.error(f'An error occurred: {e}')
            flash(f'An error occurred: {str(e)}', 'danger')

        return redirect(url_for('login'))
    
    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except SignatureExpired:
        flash('The password reset link has expired.', 'danger')
        return redirect(url_for('forgot_password'))
    except BadSignature:
        flash('The password reset link is invalid.', 'danger')
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        new_password = request.form['password']
        patients = load_patients()
        patients[email]['password'] = new_password
        save_patients(patients)
        flash('Your password has been updated!', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html')
