from setuptools import setup

package_name = 'renvros2_demo'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ysuga',
    maintainer_email='ysuga@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'twist_pub = renvros2_demo.velocity_send_device:main',
            'pose_sub = renvros2_demo.pose_receive_device:main',
            'fibonacci_action = renvros2_demo.fibonacci_action_device:main',
            'fibonacci_server = renvros2_demo.fibonacci_server:main',
            'spawn_cli = renvros2_demo.turtle_spawn:main',
            'mobile_action = renvros2_demo.turtlebot3_demo:main',
            'mobile_cancel = renvros2_demo.mobile_cancel_gui_device:main'
        ],
    },
)
