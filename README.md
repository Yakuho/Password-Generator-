# Password-Generator-密令生成器
## 可自定义密码组成；
例如：密码组成为：'0123456789', '01234567890zxcasd', '!@#$%^&*()1234567890' , ......

## 可分发密令子遍历任务；
因为有时候长度过于长的原因，分割遍历任务十分必要，例如将3位长的密码，密码组合为'0123456789'，分割为3部分，则每个部分平均只需遍历333次

## 可自定义密令长度
可根据传入密令长度自定义生成任意长度密令

## 可增加域密令并指定域位置
通过配置域文件并指定域位置，即可拿到遍历密令

## 可读取密令文件直接生成密令
通过传入文件名数组遍历所有文件

## 可读取密令文件并指定密令文件内密令的位置
通过传入文件名数组遍历所有文件,再根据位置，遍历密令
